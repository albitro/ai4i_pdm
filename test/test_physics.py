# pytest
import os
import sys
import math

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.physics import (angular_velocity, mechanical_power,
                         temp_gradient, cumulative_strain)


def _approx(a, b, tol=1e-9):
    return abs(a - b) <= tol * max(1.0, abs(b))


def test_angular_velocity():
    # 60 rpm = 1 rev/s = 2*pi rad/s
    assert _approx(angular_velocity(60), 2.0 * math.pi)
    # 0 rpm -> 0 rad/s
    assert angular_velocity(0) == 0.0


def test_mechanical_power():
    # 10 Nm, 1000 rpm -> omega=2*pi*1000/60, P=10*omega
    expected = 10.0 * (2.0 * math.pi * 1000.0 / 60.0)  # = 1047.1975...
    assert _approx(mechanical_power(10, 1000), expected)
    # 토크 0 -> 동력 0
    assert mechanical_power(0, 1500) == 0.0


def test_temp_gradient():
    assert temp_gradient(310.0, 300.0) == 10.0
    assert temp_gradient(305.0, 305.0) == 0.0
    # 순서가 바뀌면 음수 (부호 검증)
    assert temp_gradient(300.0, 310.0) == -10.0


def test_cumulative_strain():
    assert cumulative_strain(100, 40) == 4000
    assert cumulative_strain(0, 76.6) == 0.0


def _run():
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    ok = 0
    for t in tests:
        try:
            t()
            print("PASS", t.__name__)
            ok += 1
        except AssertionError as e:
            print("FAIL", t.__name__, e)
    print(f"\n{ok}/{len(tests)} passed")
    return ok == len(tests)


if __name__ == "__main__":
    sys.exit(0 if _run() else 1)
