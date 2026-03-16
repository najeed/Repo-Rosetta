import pytest
import os
from unittest.mock import AsyncMock, patch
from backend.summarizer.engine import SummarizerEngine

@pytest.mark.asyncio
async def test_summarizer_anthropic_integration():
    engine = SummarizerEngine(provider="anthropic")
    entity_data = {"name": "TestFunc", "type": "function"}
    
    # Mock API Key
    os.environ["ANTHROPIC_API_KEY"] = "fake-key"
    
    mock_message = AsyncMock()
    mock_message.content = [AsyncMock(text="Claude's explanation of TestFunc")]
    
    with patch("anthropic.AsyncAnthropic") as mock_client:
        mock_client.return_value.messages.create = AsyncMock(return_value=mock_message)
        
        summary = await engine.generate_summary(entity_data)
        assert "Claude's explanation" in summary
        mock_client.return_value.messages.create.assert_called_once()

@pytest.mark.asyncio
async def test_summarizer_gemini_integration():
    engine = SummarizerEngine(provider="gemini")
    entity_data = {"name": "TestFunc", "type": "function"}
    
    # Mock API Key
    os.environ["GEMINI_API_KEY"] = "fake-key"
    
    mock_response = AsyncMock()
    mock_response.text = "Gemini's explanation of TestFunc"
    
    with patch("google.generativeai.GenerativeModel") as mock_model:
        mock_model.return_value.generate_content_async = AsyncMock(return_value=mock_response)
        
        summary = await engine.generate_summary(entity_data, approved_provider="gemini")
        assert "Gemini's explanation" in summary
        mock_model.return_value.generate_content_async.assert_called_once()

@pytest.mark.asyncio
async def test_summarizer_fallback():
    engine = SummarizerEngine(provider="anthropic")
    entity_data = {"name": "TestFunc", "type": "function"}
    
    # Remove API key
    if "ANTHROPIC_API_KEY" in os.environ:
        del os.environ["ANTHROPIC_API_KEY"]
    
    summary = await engine.generate_summary(entity_data)
    # Should fall back to heuristic summary
    assert "Standard implementation" in summary or "Core component" in summary or "Act as a" not in summary

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_summarizer_anthropic_integration())
