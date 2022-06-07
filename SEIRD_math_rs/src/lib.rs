use ndarray::prelude::*;
use numpy::{IntoPyArray, PyArray1, PyArray3, PyReadonlyArray2};
use pyo3::prelude::{pymodule, wrap_pyfunction, PyModule, PyResult, Python};
use std::collections::HashMap;

struct SeirdArgs {
    beta: f64,
    sigma: f64,
    epsilon: f64,
    f_s: f64,
    gamma_s: f64,
    gamma_a: f64,
    delta: f64,
    sum_contact: f64,
    vac_params: f64,
}

fn seird(_t: f64, y: &Array1<f64>, c: &SeirdArgs) -> Array1<f64> {
    let mut dydt = Array::zeros(6);
    let mut diff_v = c.vac_params;

    dydt[0] = -c.beta * c.sigma * y[0] * c.sum_contact - diff_v;
    dydt[1] = c.beta * c.sigma * y[0] * c.sum_contact - c.epsilon * y[1];
    dydt[2] = c.epsilon * c.f_s * y[1] - (c.gamma_s + c.delta) * y[2];
    dydt[3] = c.epsilon * (1. - c.f_s) * y[1] - c.gamma_a * y[3];
    if y[0] <= 1.0 {
        diff_v = 0.0;
    }
    dydt[4] = c.gamma_s * y[2] + c.gamma_a * y[3] + diff_v;
    dydt[5] = c.delta * y[2];
    dydt
}

fn seird_se(_t: f64, y: &Array1<f64>, c: &SeirdArgs) -> Array1<f64> {
    let mut dydt = Array::zeros(6);
    let mut diff_v = c.vac_params;

    let ratio = y[0] / (y[0] + y[1]);
    let vac_s: f64;
    let vac_e: f64;

    if diff_v != 0.0 && ratio <= 1.0 {
        vac_s = diff_v * ratio;
        vac_e = diff_v * (1.0 - ratio);
    } else {
        vac_s = 0.0;
        vac_e = 0.0;
        diff_v = 0.0;
    }

    dydt[0] = -c.beta * c.sigma * y[0] * c.sum_contact - vac_s;
    dydt[1] = c.beta * c.sigma * y[0] * c.sum_contact - c.epsilon * y[1] - vac_e;
    dydt[2] = c.epsilon * c.f_s * y[1] - (c.gamma_s + c.delta) * y[2];
    dydt[3] = c.epsilon * (1. - c.f_s) * y[1] - c.gamma_a * y[3];
    dydt[4] = c.gamma_s * y[2] + c.gamma_a * y[3] + diff_v;
    dydt[5] = c.delta * y[2];

    dydt
}

#[pymodule]
fn seird_math(_py: Python, m: &PyModule) -> PyResult<()> {
    #[pyfn(m)]
    fn solve_seird<'py>(
        py: Python<'py>,
        time_range: (f64, f64),
        y0: PyReadonlyArray2<f64>,
        coeff: PyReadonlyArray2<f64>,
        contacts: PyReadonlyArray2<f64>,
        vac_params: HashMap<String, Vec<f64>>,
        vac_e: bool,
        dt: f64,
    ) -> (&'py PyArray1<f64>, &'py PyArray3<f64>) {
        let y0 = y0.as_array();
        let coeff = coeff.as_array();
        let contacts = contacts.as_array();

        let time_points = ndarray::Array::range(time_range.0, time_range.1 + dt, dt);
        let mut y: Array3<f64> = Array3::zeros((6, time_points.len(), 8));
        for i in 0..y0.shape()[0] {
            y.slice_mut(s![i as usize, 0_usize, ..])
                .assign(&y0.slice(s![i as usize, ..]));
        }
        let beta: Array1<f64> = coeff.slice(s![0_usize, ..]).into_owned();
        let sigma: Array1<f64> = coeff.slice(s![1_usize, ..]).into_owned();
        let epsilon: Array1<f64> = coeff.slice(s![2_usize, ..]).into_owned();
        let f_s: Array1<f64> = coeff.slice(s![3_usize, ..]).into_owned();
        let gamma_s: Array1<f64> = coeff.slice(s![4_usize, ..]).into_owned();
        let gamma_a: Array1<f64> = coeff.slice(s![5_usize, ..]).into_owned();
        let delta: Array1<f64> = coeff.slice(s![6_usize, ..]).into_owned();

        if vac_params.is_empty() {
            let f = &seird;

            for t in 0..time_points.len() - 1 {
                for i in 0..8 {
                    let dt2 = dt / 2.;
                    let prev_y = y.slice(s![.., t as usize, i as usize]).to_owned();
                    let infectious = &y.slice(s![2 as usize, t as usize, ..])
                        + &y.slice(s![3 as usize, t as usize, ..]);
                    let sum_contact = contacts.slice(s![i as usize, ..]).t().dot(&infectious);

                    let args = SeirdArgs {
                        beta: beta[i],
                        sigma: sigma[i],
                        epsilon: epsilon[i],
                        f_s: f_s[i],
                        gamma_s: gamma_s[i],
                        gamma_a: gamma_a[i],
                        delta: delta[i],
                        sum_contact: sum_contact,
                        vac_params: 0.0,
                    };

                    let ct = time_points[t];
                    let k1 = f(ct, &prev_y, &args);
                    let k2 = f(ct + dt2, &(&prev_y + &k1 * dt2), &args);
                    let k3 = f(ct + dt2, &(&prev_y + &k2 * dt2), &args);
                    let k4 = f(ct + dt, &(&prev_y + &k3 * dt), &args);

                    let new_y =
                        (&prev_y + dt * (&k1 + &k2 * 2. + &k3 * 2. + &k4) / 6.).mapv(|x| x.max(0.));
                    y.slice_mut(s![.., t + 1 as usize, i as usize])
                        .assign(&new_y);
                }
            }
        } else {
            if vac_e {
                let f = &seird_se;
                for t in 0..time_points.len() - 1 {
                    for i in 0..8 {
                        let dt2 = dt / 2.;
                        let prev_y = y.slice(s![.., t as usize, i as usize]).to_owned();
                        let infectious = &y.slice(s![2 as usize, t as usize, ..])
                            + &y.slice(s![3 as usize, t as usize, ..]);
                        let sum_contact = contacts.slice(s![i as usize, ..]).t().dot(&infectious);
                        let vac_param: f64;

                        if vac_params[&("age_grp_".to_string() + &(i + 1).to_string())][1]
                            <= time_points[t]
                            && time_points[t]
                                < vac_params[&("age_grp_".to_string() + &(i + 1).to_string())][2]
                                    + 1.0
                        {
                            vac_param = vac_params["eff"][0]
                                * vac_params[&("age_grp_".to_string() + &(i + 1).to_string())][0];
                        } else {
                            vac_param = 0.0;
                        }

                        let args = SeirdArgs {
                            beta: beta[i],
                            sigma: sigma[i],
                            epsilon: epsilon[i],
                            f_s: f_s[i],
                            gamma_s: gamma_s[i],
                            gamma_a: gamma_a[i],
                            delta: delta[i],
                            sum_contact: sum_contact,
                            vac_params: vac_param,
                        };

                        let ct = time_points[t];
                        let k1 = f(ct, &prev_y, &args);
                        let k2 = f(ct + dt2, &(&prev_y + &k1 * dt2), &args);
                        let k3 = f(ct + dt2, &(&prev_y + &k2 * dt2), &args);
                        let k4 = f(ct + dt, &(&prev_y + &k3 * dt), &args);

                        let new_y = (&prev_y + dt * (&k1 + &k2 * 2. + &k3 * 2. + &k4) / 6.)
                            .mapv(|x| x.max(0.));
                        y.slice_mut(s![.., t + 1 as usize, i as usize])
                            .assign(&new_y);
                    }
                }
            } else {
                let f = &seird;
                for t in 0..time_points.len() - 1 {
                    for i in 0..8 {
                        let dt2 = dt / 2.;
                        let prev_y = y.slice(s![.., t as usize, i as usize]).to_owned();
                        let infectious = &y.slice(s![2 as usize, t as usize, ..])
                            + &y.slice(s![3 as usize, t as usize, ..]);
                        let sum_contact = contacts.slice(s![i as usize, ..]).t().dot(&infectious);
                        let vac_param: f64;

                        if vac_params[&("age_grp_".to_string() + &(i + 1).to_string())][1]
                            <= time_points[t]
                            && time_points[t]
                                < vac_params[&("age_grp_".to_string() + &(i + 1).to_string())][2]
                                    + 1.0
                        {
                            vac_param = vac_params["eff"][0]
                                * vac_params[&("age_grp_".to_string() + &(i + 1).to_string())][0];
                        } else {
                            vac_param = 0.0;
                        }

                        let args = SeirdArgs {
                            beta: beta[i],
                            sigma: sigma[i],
                            epsilon: epsilon[i],
                            f_s: f_s[i],
                            gamma_s: gamma_s[i],
                            gamma_a: gamma_a[i],
                            delta: delta[i],
                            sum_contact: sum_contact,
                            vac_params: vac_param,
                        };

                        let ct = time_points[t];
                        let k1 = f(ct, &prev_y, &args);
                        let k2 = f(ct + dt2, &(&prev_y + &k1 * dt2), &args);
                        let k3 = f(ct + dt2, &(&prev_y + &k2 * dt2), &args);
                        let k4 = f(ct + dt, &(&prev_y + &k3 * dt), &args);

                        let new_y = (&prev_y + dt * (&k1 + &k2 * 2. + &k3 * 2. + &k4) / 6.)
                            .mapv(|x| x.max(0.));
                        y.slice_mut(s![.., t + 1 as usize, i as usize])
                            .assign(&new_y);
                    }
                }
            }
        }
        (time_points.into_pyarray(py), y.into_pyarray(py))
    }
    m.add_wrapped(wrap_pyfunction!(solve_seird))?;
    Ok(())
}
