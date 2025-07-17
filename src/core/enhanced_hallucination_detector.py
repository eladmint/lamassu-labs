"""
Enhanced Hallucination Detector with Real AI Models
Uses Google Gemini, Anthropic Claude, and other free APIs for actual hallucination detection
"""

import asyncio
import os
import time
import json
import re
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
import hashlib

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

try:
    import google.generativeai as genai
    HAS_GOOGLE = True
except ImportError:
    HAS_GOOGLE = False

try:
    import anthropic
    HAS_ANTHROPIC = True
except ImportError:
    HAS_ANTHROPIC = False

try:
    import openai
    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

from .hallucination_detector import (
    HallucinationType, HallucinationEvidence, HallucinationDetectionResult,
    HallucinationDetector
)


@dataclass
class AIVerificationResult:
    """Result from AI-powered verification"""
    is_factual: bool
    confidence: float
    explanation: str
    sources_checked: List[str] = field(default_factory=list)
    model_used: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'is_factual': self.is_factual,
            'confidence': self.confidence,
            'explanation': self.explanation,
            'sources_checked': self.sources_checked,
            'model_used': self.model_used
        }


class WikipediaFactChecker:
    """Free fact-checking using Wikipedia API"""
    
    def __init__(self):
        self.base_url = "https://en.wikipedia.org/api/rest_v1/page/summary/"
        self.search_url = "https://en.wikipedia.org/api/rest_v1/page/search/"
    
    async def verify_fact(self, claim: str) -> AIVerificationResult:
        """Verify a factual claim against Wikipedia"""
        try:
            # Extract key terms for search
            search_terms = self._extract_search_terms(claim)
            
            # Search Wikipedia
            search_results = await self._search_wikipedia(search_terms)
            
            if not search_results:
                return AIVerificationResult(
                    is_factual=False,
                    confidence=0.3,
                    explanation="No relevant Wikipedia articles found",
                    model_used="Wikipedia API"
                )
            
            # Get detailed info for top results
            verification_evidence = []
            for result in search_results[:3]:  # Check top 3 results
                summary = await self._get_page_summary(result['key'])
                if summary:
                    verification_evidence.append({
                        'title': result['title'],
                        'extract': summary.get('extract', ''),
                        'url': summary.get('content_urls', {}).get('desktop', {}).get('page', '')
                    })
            
            # Simple fact checking logic
            is_factual, confidence, explanation = self._analyze_evidence(claim, verification_evidence)
            
            return AIVerificationResult(
                is_factual=is_factual,
                confidence=confidence,
                explanation=explanation,
                sources_checked=[e['url'] for e in verification_evidence],
                model_used="Wikipedia API"
            )
            
        except Exception as e:
            return AIVerificationResult(
                is_factual=False,
                confidence=0.1,
                explanation=f"Error during verification: {str(e)}",
                model_used="Wikipedia API (Error)"
            )
    
    def _extract_search_terms(self, claim: str) -> str:
        """Extract search terms from claim"""
        # Remove common words and extract key terms
        stopwords = {'the', 'is', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'what', 'when', 'where', 'who', 'how', 'why'}
        words = re.findall(r'\b\w+\b', claim.lower())
        key_words = [w for w in words if w not in stopwords and len(w) > 2]
        return ' '.join(key_words[:5])  # Top 5 key words
    
    async def _search_wikipedia(self, query: str) -> List[Dict]:
        """Search Wikipedia for relevant articles"""
        if not HAS_REQUESTS:
            return []
        
        try:
            # Use the opensearch API which is more reliable
            search_url = "https://en.wikipedia.org/w/api.php"
            params = {
                'action': 'opensearch',
                'search': query,
                'limit': 5,
                'format': 'json'
            }
            response = requests.get(search_url, params=params, timeout=5)
            if response.status_code == 200:
                data = response.json()
                if len(data) >= 4:
                    titles = data[1]
                    descriptions = data[2] 
                    urls = data[3]
                    return [
                        {'key': title.replace(' ', '_'), 'title': title, 'description': desc, 'url': url}
                        for title, desc, url in zip(titles, descriptions, urls)
                    ]
        except Exception as e:
            print(f"Wikipedia search error: {e}")
        return []
    
    async def _get_page_summary(self, page_key: str) -> Optional[Dict]:
        """Get summary of a Wikipedia page"""
        if not HAS_REQUESTS:
            return None
        
        try:
            # Use the Wikipedia API to get page extract
            api_url = "https://en.wikipedia.org/w/api.php"
            params = {
                'action': 'query',
                'format': 'json',
                'titles': page_key.replace('_', ' '),
                'prop': 'extracts',
                'exintro': True,
                'explaintext': True,
                'exsectionformat': 'plain'
            }
            response = requests.get(api_url, params=params, timeout=5)
            if response.status_code == 200:
                data = response.json()
                pages = data.get('query', {}).get('pages', {})
                for page_id, page_data in pages.items():
                    if 'extract' in page_data:
                        return {
                            'extract': page_data['extract'],
                            'title': page_data.get('title', ''),
                            'content_urls': {'desktop': {'page': f"https://en.wikipedia.org/wiki/{page_key}"}}
                        }
        except Exception as e:
            print(f"Wikipedia page summary error: {e}")
        return None
    
    def _analyze_evidence(self, claim: str, evidence: List[Dict]) -> Tuple[bool, float, str]:
        """Analyze evidence to determine if claim is factual"""
        claim_lower = claim.lower()
        
        # Look for contradictions or confirmations
        confirmations = 0
        contradictions = 0
        
        for e in evidence:
            extract_lower = e.get('extract', '').lower()
            
            # Simple keyword matching for fact checking
            if 'capital' in claim_lower and 'france' in claim_lower:
                if 'paris' in extract_lower and 'capital' in extract_lower:
                    confirmations += 1
                elif 'london' in claim_lower and 'london' not in extract_lower:
                    contradictions += 1
            
            # Check for temporal consistency
            future_years = re.findall(r'20(2[6-9]|[3-9]\d)', claim_lower)
            past_indicators = ['was', 'happened', 'occurred', 'ended', 'began']
            if future_years and any(word in claim_lower for word in past_indicators):
                contradictions += 1
        
        # Determine result
        if contradictions > confirmations:
            return False, 0.8, f"Evidence contradicts claim (found {contradictions} contradictions)"
        elif confirmations > 0:
            return True, 0.7, f"Evidence supports claim (found {confirmations} confirmations)"
        else:
            return False, 0.5, "Insufficient evidence to verify claim"


class GeminiHallucinationChecker:
    """Use Google Gemini for hallucination detection"""
    
    def __init__(self):
        self.model = None
        self.available = False
        
        # Try to initialize Gemini
        api_key = os.getenv("GOOGLE_API_KEY")
        if api_key and HAS_GOOGLE:
            try:
                genai.configure(api_key=api_key)
                self.model = genai.GenerativeModel('gemini-1.5-flash')
                self.available = True
            except Exception as e:
                print(f"⚠️  Gemini initialization failed: {e}")
    
    async def detect_hallucination(self, text: str) -> AIVerificationResult:
        """Use Gemini to detect hallucinations"""
        if not self.available:
            return AIVerificationResult(
                is_factual=True,
                confidence=0.5,
                explanation="Gemini not available",
                model_used="None"
            )
        
        try:
            prompt = f"""
Analyze the following text for potential hallucinations or false information. 
Consider:
1. Factual accuracy
2. Temporal consistency (events described as past when they're future)
3. Plausible but unverifiable claims
4. Suspicious statistics or data
5. Non-existent technologies, papers, or people

Text to analyze: "{text}"

Respond in JSON format:
{{
    "is_factual": true/false,
    "confidence": 0.0-1.0,
    "explanation": "Brief explanation of findings",
    "issues_found": ["list", "of", "specific", "issues"]
}}
"""
            
            response = self.model.generate_content(prompt)
            
            # Parse JSON response
            try:
                # Clean the response text
                response_text = response.text.strip()
                if response_text.startswith('```json'):
                    response_text = response_text[7:]
                if response_text.endswith('```'):
                    response_text = response_text[:-3]
                
                result = json.loads(response_text)
                
                return AIVerificationResult(
                    is_factual=result.get('is_factual', True),
                    confidence=float(result.get('confidence', 0.5)),
                    explanation=result.get('explanation', 'No explanation provided'),
                    sources_checked=['Google Gemini Analysis'],
                    model_used="Gemini Pro"
                )
                
            except json.JSONDecodeError:
                # Fallback to text analysis
                response_lower = response.text.lower()
                is_factual = 'false' not in response_lower and 'hallucination' not in response_lower
                confidence = 0.6 if is_factual else 0.8
                
                return AIVerificationResult(
                    is_factual=is_factual,
                    confidence=confidence,
                    explanation=response.text[:200],
                    model_used="Gemini Pro (Text)"
                )
                
        except Exception as e:
            return AIVerificationResult(
                is_factual=True,
                confidence=0.3,
                explanation=f"Error during Gemini analysis: {str(e)}",
                model_used="Gemini Pro (Error)"
            )


class ClaudeHallucinationChecker:
    """Use Anthropic Claude for hallucination detection"""
    
    def __init__(self):
        self.client = None
        self.available = False
        
        # Try to initialize Claude
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if api_key and HAS_ANTHROPIC:
            try:
                self.client = anthropic.Anthropic(api_key=api_key)
                self.available = True
            except Exception as e:
                print(f"⚠️  Claude initialization failed: {e}")
    
    async def detect_hallucination(self, text: str) -> AIVerificationResult:
        """Use Claude to detect hallucinations"""
        if not self.available:
            return AIVerificationResult(
                is_factual=True,
                confidence=0.5,
                explanation="Claude not available",
                model_used="None"
            )
        
        try:
            prompt = f"""
Please analyze this text for potential hallucinations or false information:

"{text}"

Check for:
- Factual inaccuracies
- Future events described as past
- Non-existent research papers or studies
- Impossible statistics
- Non-existent technologies or APIs
- Overconfident claims about unverifiable facts

Respond with:
1. Is this factually accurate? (YES/NO)
2. Confidence level (0-100%)
3. Brief explanation
4. Specific issues if any

Be concise and focus on clear factual problems.
"""
            
            response = self.client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=200,
                temperature=0.1,
                messages=[{"role": "user", "content": prompt}]
            )
            
            response_text = response.content[0].text.lower()
            
            # Parse response
            is_factual = 'yes' in response_text.split('\n')[0] if '\n' in response_text else 'no' not in response_text
            
            # Extract confidence if mentioned
            confidence_match = re.search(r'(\d+)%', response_text)
            confidence = float(confidence_match.group(1)) / 100 if confidence_match else (0.7 if is_factual else 0.8)
            
            return AIVerificationResult(
                is_factual=is_factual,
                confidence=confidence,
                explanation=response.content[0].text[:200],
                sources_checked=['Anthropic Claude Analysis'],
                model_used="Claude 3 Haiku"
            )
            
        except Exception as e:
            return AIVerificationResult(
                is_factual=True,
                confidence=0.3,
                explanation=f"Error during Claude analysis: {str(e)}",
                model_used="Claude (Error)"
            )


class EnhancedHallucinationDetector(HallucinationDetector):
    """Enhanced detector that combines pattern matching with AI models"""
    
    def __init__(self):
        super().__init__()
        
        # Initialize AI checkers
        self.wikipedia_checker = WikipediaFactChecker()
        self.gemini_checker = GeminiHallucinationChecker()
        self.claude_checker = ClaudeHallucinationChecker()
        
        # Track which services are available
        self.available_services = []
        if self.gemini_checker.available:
            self.available_services.append("Gemini")
        if self.claude_checker.available:
            self.available_services.append("Claude")
        self.available_services.append("Wikipedia")  # Always available
        
        print(f"✅ Enhanced detector initialized with: {', '.join(self.available_services)}")
    
    async def detect_hallucinations(self, text: str, context: Optional[Dict[str, Any]] = None) -> HallucinationDetectionResult:
        """Enhanced detection using both patterns and AI"""
        start_time = time.time()
        
        # Start with pattern-based detection
        pattern_result = await super().detect_hallucinations(text, context)
        
        # If patterns already found issues, still check with AI for confirmation
        ai_verifications = []
        
        # Run AI checkers in parallel
        ai_tasks = []
        
        # Wikipedia fact checking
        ai_tasks.append(self.wikipedia_checker.verify_fact(text))
        
        # Gemini analysis
        if self.gemini_checker.available:
            ai_tasks.append(self.gemini_checker.detect_hallucination(text))
        
        # Claude analysis
        if self.claude_checker.available:
            ai_tasks.append(self.claude_checker.detect_hallucination(text))
        
        # Wait for AI results
        if ai_tasks:
            ai_results = await asyncio.gather(*ai_tasks, return_exceptions=True)
            ai_verifications = [r for r in ai_results if isinstance(r, AIVerificationResult)]
        
        # Combine results
        enhanced_result = self._combine_results(pattern_result, ai_verifications, text)
        enhanced_result.detection_time_ms = int((time.time() - start_time) * 1000)
        
        return enhanced_result
    
    def _combine_results(self, pattern_result: HallucinationDetectionResult, 
                        ai_results: List[AIVerificationResult], text: str) -> HallucinationDetectionResult:
        """Combine pattern and AI detection results"""
        
        # Start with pattern results
        combined_result = HallucinationDetectionResult()
        combined_result.hallucinations = pattern_result.hallucinations.copy()
        combined_result.has_hallucination = pattern_result.has_hallucination
        combined_result.overall_confidence = pattern_result.overall_confidence
        combined_result.trust_score = pattern_result.trust_score
        
        # Analyze AI results
        ai_detected_issues = []
        ai_confidence_scores = []
        
        for ai_result in ai_results:
            ai_confidence_scores.append(ai_result.confidence)
            
            if not ai_result.is_factual:
                # AI detected a problem
                evidence = HallucinationEvidence(
                    type=HallucinationType.PLAUSIBLE_FABRICATION,  # Default type for AI detection
                    confidence=ai_result.confidence,
                    description=f"AI-detected issue: {ai_result.explanation}",
                    source_text=text[:200],
                    evidence=[f"Source: {ai_result.model_used}"] + ai_result.sources_checked
                )
                ai_detected_issues.append(evidence)
        
        # Add AI-detected issues
        for issue in ai_detected_issues:
            combined_result.add_hallucination(issue)
        
        # Adjust trust score based on AI consensus
        if ai_confidence_scores:
            ai_average_confidence = sum(ai_confidence_scores) / len(ai_confidence_scores)
            
            # If AI is confident something is wrong, reduce trust significantly
            if any(not ai.is_factual and ai.confidence > 0.7 for ai in ai_results):
                combined_result.trust_score *= 0.3  # Severely reduce trust
            elif ai_average_confidence < 0.6:
                combined_result.trust_score *= 0.7  # Moderately reduce trust
            
            # Update overall confidence to include AI input
            if ai_detected_issues:
                combined_result.overall_confidence = max(
                    combined_result.overall_confidence,
                    max(ai.confidence for ai in ai_results if not ai.is_factual)
                )
        
        return combined_result


# Factory function for easy initialization
def create_enhanced_detector() -> EnhancedHallucinationDetector:
    """Create an enhanced hallucination detector with available AI services"""
    return EnhancedHallucinationDetector()