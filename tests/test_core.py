def validate_response_schema(data):
    assert isinstance(data, dict)
    assert "answer" in data and isinstance(data["answer"], str)
    assert "confidence" in data and isinstance(data["confidence"], (int, float))
    assert "actions" in data and isinstance(data["actions"], list)

def test_response_schema_valid():
    sample = {
        "answer": "Texto de prueba",
        "confidence": 0.8,
        "actions": ["accion1", "accion2"]
    }
    validate_response_schema(sample)