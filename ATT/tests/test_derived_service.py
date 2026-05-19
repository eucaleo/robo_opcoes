from services.derived_service import _resolve_storage_key, _merge_meta


def test_resolve_storage_key_should_prefer_aba_when_present():
    result = _resolve_storage_key(
        aba="BOVA11",
        structure_id=7,
        structure_name="BOVA11 Condor Maio/2026",
        underlying_asset="BOVA11",
    )

    assert result == "BOVA11"


def test_resolve_storage_key_should_fallback_to_structure_id():
    result = _resolve_storage_key(
        aba=None,
        structure_id=7,
        structure_name="BOVA11 Condor Maio/2026",
        underlying_asset="BOVA11",
    )

    assert result == "structure:7"


def test_merge_meta_should_enrich_with_canonical_identity():
    result = _merge_meta(
        meta={"origin": "test"},
        structure_id=7,
        structure_name="BOVA11 Condor Maio/2026",
        underlying_asset="BOVA11",
        reference_date="2026-05-18",
        input_meta={"legs_source": "canonical"},
    )

    assert result["origin"] == "test"
    assert result["structure_id"] == 7
    assert result["structure_name"] == "BOVA11 Condor Maio/2026"
    assert result["underlying_asset"] == "BOVA11"
    assert result["reference_date"] == "2026-05-18"
    assert result["input_meta"]["legs_source"] == "canonical"
