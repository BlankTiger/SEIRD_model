use ndarray::prelude::*;
use numpy::{IntoPyArray, PyArray1, PyArray3, PyReadonlyArray2};
use pyo3::prelude::{pymodule, wrap_pyfunction, PyModule, PyResult, Python};
use std::collections::HashMap;

// #[pyclass]
// struct Solution {
//     t: PyArray1<f64>,
//     y: PyArray2<f64>,
// }

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

fn SEIRD(t: f64, y: &Array1<f64>, c: &SeirdArgs) -> Array1<f64> {
    let mut dydt = Array::zeros(6);
    let mut diff_v = c.vac_params;

    if y[0] - c.beta * c.sigma * y[0] * c.sum_contact - diff_v < 0.0 {
        diff_v = y[0]
    }

    dydt[0] = -c.beta * c.sigma * y[0] * c.sum_contact - diff_v;
    dydt[1] = c.beta * c.sigma * y[0] * c.sum_contact - c.epsilon * y[1];
    dydt[2] = c.epsilon * c.f_s * y[1] - (c.gamma_s + c.delta) * y[2];
    dydt[3] = c.epsilon * (1. - c.f_s) * y[1] - c.gamma_a * y[3];
    dydt[4] = c.gamma_s * y[2] + c.gamma_a * y[3] + diff_v;
    dydt[5] = c.delta * y[2];
    dydt
}

fn SEIRD_SE(t: f64, y: &Array1<f64>, c: &SeirdArgs) -> Array1<f64> {
    let mut dydt = Array::zeros(6);
    let mut diff_v = c.vac_params;

    let mut vac_S = y[0] / (y[0] + y[1]);
    let mut vac_E = 0.0;
    let mut corr = 0.0;

    if diff_v != 0.0 && vac_S < 1.0 {
        vac_S = diff_v * vac_S;
        vac_E = diff_v - vac_S;
    } else {
        vac_S = 0.0;
        vac_E = 0.0;
        diff_v = 0.0;
    }

    if y[0] - c.beta * c.sigma * y[0] * c.sum_contact - vac_S < 0.0 {
        corr = y[0];
    }

    dydt[0] = -c.beta * c.sigma * y[0] * c.sum_contact - vac_S - corr;

    if y[1] * c.epsilon + vac_E > y[1] + c.beta * c.sigma * y[0] * c.sum_contact {
        corr = y[1];
    }

    dydt[1] = c.beta * c.sigma * y[0] * c.sum_contact - c.epsilon * y[1] - vac_E - corr;
    dydt[2] = c.epsilon * c.f_s * y[1] - (c.gamma_s + c.delta) * y[2];
    dydt[3] = c.epsilon * (1. - c.f_s) * y[1] - c.gamma_a * y[3];
    dydt[4] = c.gamma_s * y[2] + c.gamma_a * y[3] + diff_v;
    dydt[5] = c.delta * y[2];

    dydt
}

#[pymodule]
fn seird_math(_py: Python, m: &PyModule) -> PyResult<()> {
    #[pyfn(m)]
    fn solve_SEIRD<'py>(
        py: Python<'py>,
        time_range: (f64, f64),
        y0: PyReadonlyArray2<f64>,
        coeff: PyReadonlyArray2<f64>,
        contacts: PyReadonlyArray2<f64>,
        vac_params: HashMap<String, Vec<f64>>,
        vac_e: bool,
    ) -> (&'py PyArray1<f64>, &'py PyArray3<f64>) {
        let y0 = y0.as_array();
        let coeff = coeff.as_array();
        let contacts = contacts.as_array();

        let dt = 1.0;
        let time_points = ndarray::Array::range(time_range.0, time_range.1 + 1., dt);
        let mut seird: Array3<f64> = Array3::zeros((6, time_points.len(), 8));
        for i in 0..y0.shape()[0] {
            seird
                .slice_mut(s![i as usize, 0_usize, ..])
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
            let f = &SEIRD;
            let vac_param = 0.0;

            for t in 0..time_points.len() - 1 {
                for i in 0..8 {
                    let dt2 = dt / 2.;
                    let prev_y = seird.slice(s![.., t as usize, i as usize]).to_owned();
                    let I = &seird.slice(s![2 as usize, t as usize, ..])
                        + &seird.slice(s![3 as usize, t as usize, ..]);
                    let sum_contact = contacts.slice(s![i as usize, ..]).t().dot(&I);

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

                    let ct = t as f64;
                    let k1 = f(ct, &prev_y, &args);
                    let k2 = f(ct + dt2, &(&prev_y + &k1 * dt2), &args);
                    let k3 = f(ct + dt2, &(&prev_y + &k2 * dt2), &args);
                    let k4 = f(ct + dt, &(&prev_y + &k3 * dt), &args);

                    let new_y =
                        (&prev_y + dt * (&k1 + &k2 * 2. + &k3 * 2. + &k4) / 6.).mapv(|x| x.max(0.));
                    seird
                        .slice_mut(s![.., t + 1 as usize, i as usize])
                        .assign(&new_y);
                }
            }
        } else {
            if vac_e {
                let f = &SEIRD_SE;
                for t in 0..time_points.len() - 1 {
                    for i in 0..8 {
                        let dt2 = dt / 2.;
                        let prev_y = seird.slice(s![.., t as usize, i as usize]).to_owned();
                        let I = &seird.slice(s![2 as usize, t as usize, ..])
                            + &seird.slice(s![3 as usize, t as usize, ..]);
                        let sum_contact = contacts.slice(s![i as usize, ..]).t().dot(&I);
                        let mut vac_param: f64 = 0.0;

                        if vac_params[&("age_grp_".to_string() + &(i + 1).to_string())][1]
                            <= t as f64
                            && t as f64
                                <= vac_params[&("age_grp_".to_string() + &(i + 1).to_string())][2]
                        {
                            vac_param = vac_params["eff"][0]
                                * vac_params[&("age_grp_".to_string() + &(i + 1).to_string())][0];
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

                        let ct = t as f64;
                        let k1 = f(ct, &prev_y, &args);
                        let k2 = f(ct + dt2, &(&prev_y + &k1 * dt2), &args);
                        let k3 = f(ct + dt2, &(&prev_y + &k2 * dt2), &args);
                        let k4 = f(ct + dt, &(&prev_y + &k3 * dt), &args);

                        let new_y = (&prev_y + dt * (&k1 + &k2 * 2. + &k3 * 2. + &k4) / 6.)
                            .mapv(|x| x.max(0.));
                        seird
                            .slice_mut(s![.., t + 1 as usize, i as usize])
                            .assign(&new_y);
                    }
                }
            } else {
                let f = &SEIRD;
                for t in 0..time_points.len() - 1 {
                    for i in 0..8 {
                        let dt2 = dt / 2.;
                        let prev_y = seird.slice(s![.., t as usize, i as usize]).to_owned();
                        let I = &seird.slice(s![2 as usize, t as usize, ..])
                            + &seird.slice(s![3 as usize, t as usize, ..]);
                        let sum_contact = contacts.slice(s![i as usize, ..]).t().dot(&I);
                        let mut vac_param: f64 = 0.0;

                        if vac_params[&("age_grp_".to_string() + &(i + 1).to_string())][1]
                            <= t as f64
                            && t as f64
                                <= vac_params[&("age_grp_".to_string() + &(i + 1).to_string())][2]
                        {
                            vac_param = vac_params["eff"][0]
                                * vac_params[&("age_grp_".to_string() + &(i + 1).to_string())][0];
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

                        let ct = t as f64;
                        let k1 = f(ct, &prev_y, &args);
                        let k2 = f(ct + dt2, &(&prev_y + &k1 * dt2), &args);
                        let k3 = f(ct + dt2, &(&prev_y + &k2 * dt2), &args);
                        let k4 = f(ct + dt, &(&prev_y + &k3 * dt), &args);

                        let new_y = (&prev_y + dt * (&k1 + &k2 * 2. + &k3 * 2. + &k4) / 6.)
                            .mapv(|x| x.max(0.));
                        seird
                            .slice_mut(s![.., t + 1 as usize, i as usize])
                            .assign(&new_y);
                    }
                }
            }
        }
        (time_points.into_pyarray(py), seird.into_pyarray(py))
    }
    m.add_wrapped(wrap_pyfunction!(solve_SEIRD))?;
    Ok(())
}

// struct MyPyArray<'a> {
//     arr: &'a numpy::PyArray<f64, ndarray::Dim<[usize; 2]>>,
// }

// unsafe impl numpy::Element for MyPyArray<'_> {}
// impl numpy::IntoPyArray for MyPyArray<'_> {}
// impl std::iter::FromIterator
