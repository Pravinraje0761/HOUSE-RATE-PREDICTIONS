"""Model and app tests. They retrain on the bundled synthetic dataset (a few seconds)."""
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import train  # noqa: E402


def test_no_feature_is_derived_from_the_price():
    # Regression: the notebook used Price_per_SqFt (= Price / Area) as an input.
    assert train.TARGET not in train.FEATURES
    assert not any("price" in f.lower() for f in train.FEATURES)


@pytest.fixture(scope="module")
def trained():
    X, y = train.load_data()
    return train.evaluate(X, y)


def test_models_reach_a_sensible_held_out_r2(trained):
    results, _ = trained
    assert results["Linear Regression"]["test_r2"] > 0.8
    for r in results.values():
        assert r["test_r2"] < 0.97, "suspiciously high: check for leakage"


def test_bigger_house_costs_more(trained):
    _, fitted = trained
    base = dict(Location="Suburban", City="Chicago", Number_of_Bedrooms=3, Number_of_Bathrooms=2,
                Number_of_Floors=2, Parking=1, Age_of_House=10, Furnishing_Status="Semi-Furnished",
                Distance_to_City_Center=10, Nearby_Schools=3, Nearby_Hospitals=2, Crime_Rate="Low",
                Property_Type="House")
    small, large = fitted["Linear Regression"].predict(
        train.build_input_frame([{**base, "Area": 1000}, {**base, "Area": 4000}]))
    assert large > small


def test_missing_values_are_handled(trained):
    _, fitted = trained
    row = {f: None for f in train.FEATURES} | {"Area": 2000, "Location": "Urban"}
    assert fitted["Linear Regression"].predict(train.build_input_frame(row))[0] > 0


def test_streamlit_app_predicts(tmp_path):
    from streamlit.testing.v1 import AppTest
    at = AppTest.from_file(str(ROOT / "app.py"), default_timeout=60).run()
    assert not at.exception
    at.button(key="predict_btn").click().run()
    assert not at.exception
    assert any("Typical error" in i.value for i in at.info)
