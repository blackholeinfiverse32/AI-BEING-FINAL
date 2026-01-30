"""
AI Being Unified - LLM Router
Standardized LLM interface supporting Claude, OpenAI, and local models
"""
import os
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from enum import Enum

class LLMProvider(Enum):
    CLAUDE = "claude"
    OPENAI = "openai"
    GROQ = "groq"
    GOOGLE = "google"
    MISTRAL = "mistral"
    LOCAL = "local"

@dataclass
class LLMResponse:
    content: str
    provider: str
    model: str
    tokens_used: int
    confidence: float = 0.8

class LLMRouter:
    def __init__(self):
        self.providers = {}
        self.default_provider = LLMProvider.CLAUDE
        self._setup_providers()
    
    def _setup_providers(self):
        """Initialize available LLM providers"""
        # Claude (Primary)
        if os.getenv("ANTHROPIC_API_KEY"):
            self.providers[LLMProvider.CLAUDE] = self._setup_claude()
        
        # OpenAI (Fallback)
        if os.getenv("OPENAI_API_KEY"):
            self.providers[LLMProvider.OPENAI] = self._setup_openai()
        
        # Groq (Fast inference)
        if os.getenv("GROQ_API_KEY"):
            self.providers[LLMProvider.GROQ] = self._setup_groq()
        
        # Google (Alternative)
        if os.getenv("GOOGLE_API_KEY"):
            self.providers[LLMProvider.GOOGLE] = self._setup_google()
        
        # Mistral (AI-ASSISTANT integration)
        if os.getenv("MISTRAL_API_KEY"):
            self.providers[LLMProvider.MISTRAL] = self._setup_mistral()
    
    def _setup_claude(self):
        try:
            import anthropic
            return anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        except ImportError:
            return None
    
    def _setup_openai(self):
        try:
            import openai
            return openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        except ImportError:
            return None
    
    def _setup_groq(self):
        try:
            import groq
            return groq.Groq(api_key=os.getenv("GROQ_API_KEY"))
        except ImportError:
            return None
    
    def _setup_google(self):
        try:
            import google.generativeai as genai
            genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
            return genai
        except ImportError:
            return None
    
    def _setup_mistral(self):
        """Setup Mistral AI provider (from AI-ASSISTANT integration)"""
        try:
            from mistralai.client import MistralClient
            return MistralClient(api_key=os.getenv("MISTRAL_API_KEY"))
        except ImportError:
            return None
    
    async def generate(self, 
                      prompt: str, 
                      provider: Optional[LLMProvider] = None,
                      model: Optional[str] = None,
                      max_tokens: int = 1000,
                      temperature: float = 0.7) -> LLMResponse:
        """Generate response using specified or default provider"""
        
        if provider is None:
            provider = self.default_provider
        
        if provider not in self.providers or self.providers[provider] is None:
            # Fallback to available provider
            for fallback_provider in [LLMProvider.CLAUDE, LLMProvider.OPENAI, LLMProvider.GROQ]:
                if fallback_provider in self.providers and self.providers[fallback_provider]:
                    provider = fallback_provider
                    break
            else:
                raise RuntimeError("No LLM providers available")
        
        try:
            if provider == LLMProvider.CLAUDE:
                return await self._generate_claude(prompt, model or "claude-3-sonnet-20240229", max_tokens, temperature)
            elif provider == LLMProvider.OPENAI:
                return await self._generate_openai(prompt, model or "gpt-3.5-turbo", max_tokens, temperature)
            elif provider == LLMProvider.GROQ:
                return await self._generate_groq(prompt, model or "mixtral-8x7b-32768", max_tokens, temperature)
            elif provider == LLMProvider.GOOGLE:
                return await self._generate_google(prompt, model or "gemini-pro", max_tokens, temperature)
            elif provider == LLMProvider.MISTRAL:
                return await self._generate_mistral(prompt, model or "mistral-medium", max_tokens, temperature)
        except Exception as e:
            # Fallback to mock response for demo
            return LLMResponse(
                content=f"Mock response for: {prompt[:50]}...",
                provider=provider.value,
                model=model or "mock",
                tokens_used=len(prompt.split()),
                confidence=0.5
            )
    
    async def _generate_claude(self, prompt: str, model: str, max_tokens: int, temperature: float) -> LLMResponse:
        client = self.providers[LLMProvider.CLAUDE]
        response = client.messages.create(
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
            messages=[{"role": "user", "content": prompt}]
        )
        
        return LLMResponse(
            content=response.content[0].text,
            provider="claude",
            model=model,
            tokens_used=response.usage.input_tokens + response.usage.output_tokens,
            confidence=0.9
        )
    
    async def _generate_openai(self, prompt: str, model: str, max_tokens: int, temperature: float) -> LLMResponse:
        client = self.providers[LLMProvider.OPENAI]
        response = client.chat.completions.create(
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
            messages=[{"role": "user", "content": prompt}]
        )
        
        return LLMResponse(
            content=response.choices[0].message.content,
            provider="openai",
            model=model,
            tokens_used=response.usage.total_tokens,
            confidence=0.85
        )
    
    async def _generate_groq(self, prompt: str, model: str, max_tokens: int, temperature: float) -> LLMResponse:
        client = self.providers[LLMProvider.GROQ]
        response = client.chat.completions.create(
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
            messages=[{"role": "user", "content": prompt}]
        )
        
        return LLMResponse(
            content=response.choices[0].message.content,
            provider="groq",
            model=model,
            tokens_used=response.usage.total_tokens,
            confidence=0.8
        )
    
    async def _generate_google(self, prompt: str, model: str, max_tokens: int, temperature: float) -> LLMResponse:
        genai = self.providers[LLMProvider.GOOGLE]
        model_instance = genai.GenerativeModel(model)
        response = model_instance.generate_content(prompt)
        
        return LLMResponse(
            content=response.text,
            provider="google",
            model=model,
            tokens_used=len(prompt.split()) + len(response.text.split()),
            confidence=0.8
        )
    
    async def _generate_mistral(self, prompt: str, model: str, max_tokens: int, temperature: float) -> LLMResponse:
        """Generate response using Mistral AI (from AI-ASSISTANT integration)"""
        import asyncio
        client = self.providers[LLMProvider.MISTRAL]
        
        # Mistral client is synchronous, run in thread
        response = await asyncio.to_thread(
            client.chat,
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            temperature=temperature
        )
        
        return LLMResponse(
            content=response.choices[0].message.content,
            provider="mistral",
            model=model,
            tokens_used=len(prompt.split()) + len(response.choices[0].message.content.split()),
            confidence=0.85
        )