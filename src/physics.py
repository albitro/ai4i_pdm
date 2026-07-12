import numpy as np

COL_OMEGA = "Angular velocity [rad/s]"
COL_POWER = "Mechanical power [W]"
COL_DT = "Temp difference [K]"
COL_STRAIN = "Overstrain [min*Nm]"


def angular_velocity(speed_rpm):
    # 회전속도[rpm] -> 각속도 omega [rad/s]. omega = 2*pi*N/60
    return 2.0 * np.pi * speed_rpm / 60.0


def mechanical_power(torque_nm, speed_rpm):
    # 기계 동력 P = tau*omega [W] 회전기계가 내는 일률
    return torque_nm * angular_velocity(speed_rpm)


def temp_gradient(process_temp_k, air_temp_k):
    # 온도 구배 dT = 공정온도 - 공기온도 [K]. 방열을 좌우
    return process_temp_k - air_temp_k


def cumulative_strain(tool_wear_min, torque_nm):
    # 누적 응력 proxy = 공구마모 x 토크 [min*Nm]. 과부하 파손 지표
    return tool_wear_min * torque_nm


def add_physics_features(df):
    out = df.copy()
    out[COL_OMEGA] = angular_velocity(out["Rotational speed [rpm]"])
    out[COL_POWER] = mechanical_power(out["Torque [Nm]"], out["Rotational speed [rpm]"])
    out[COL_DT] = temp_gradient(out["Process temperature [K]"], out["Air temperature [K]"])
    out[COL_STRAIN] = cumulative_strain(out["Tool wear [min]"], out["Torque [Nm]"])
    return out


def check_invariants(feat):
    N = feat["Rotational speed [rpm]"]
    tau = feat["Torque [Nm]"]
    wear = feat["Tool wear [min]"]
    return {
        "omega > 0": bool((feat[COL_OMEGA] > 0).all()),
        "P > 0": bool((feat[COL_POWER] > 0).all()),
        "dT > 0 (process hotter than ambient)": bool((feat[COL_DT] > 0).all()),
        "omega == 2*pi*N/60": bool(np.allclose(feat[COL_OMEGA], 2.0 * np.pi * N / 60.0)),
        "P == tau*omega": bool(np.allclose(feat[COL_POWER], tau * feat[COL_OMEGA])),
        "strain == wear*tau": bool(np.allclose(feat[COL_STRAIN], wear * tau)),
    }
