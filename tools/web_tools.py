"""
AI Being Unified - Web Tools
Web search, browsing, and information retrieval tools
"""
import requests
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
import json
import time
from urllib.parse import urljoin, urlparse
import re

@dataclass
class SearchResult:
    title: str
    url: str
    snippet: str
    relevance_score: float

@dataclass
class WebPageContent:
    url: str
    title: str
    content: str
    links: List[str]
    metadata: Dict[str, Any]

class WebSearchTool:
    """Web search functionality"""
    
    def __init__(self):
        self.search_engines = {
            "duckduckgo": self._search_duckduckgo,
            "mock": self._mock_search  # Fallback for demo
        }
        self.default_engine = "mock"  # Use mock by default for demo
    
    def search(self, query: str, max_results: int = 5, engine: str = None) -> List[SearchResult]:
        """Search the web for information"""
        
        if not query.strip():
            return []
        
        engine = engine or self.default_engine
        
        if engine not in self.search_engines:
            engine = "mock"
        
        try:
            return self.search_engines[engine](query, max_results)
        except Exception as e:
            # Fallback to mock search
            return self._mock_search(query, max_results)
    
    def _search_duckduckgo(self, query: str, max_results: int) -> List[SearchResult]:
        """Search using DuckDuckGo (requires additional setup)"""
        # This would require the duckduckgo-search library
        # For now, return mock results
        return self._mock_search(query, max_results)
    
    def _mock_search(self, query: str, max_results: int) -> List[SearchResult]:
        """Mock search results for demonstration"""
        
        mock_results = [
            SearchResult(
                title=f"Information about {query}",
                url=f"https://example.com/search/{query.replace(' ', '-')}",
                snippet=f"Comprehensive information about {query}. This page contains detailed explanations and examples.",
                relevance_score=0.9
            ),
            SearchResult(
                title=f"{query} - Wikipedia",
                url=f"https://en.wikipedia.org/wiki/{query.replace(' ', '_')}",
                snippet=f"{query} is a topic that covers various aspects including history, applications, and current developments.",
                relevance_score=0.85
            ),
            SearchResult(
                title=f"Guide to {query}",
                url=f"https://guide.example.com/{query.replace(' ', '-')}",
                snippet=f"A comprehensive guide covering everything you need to know about {query}.",
                relevance_score=0.8
            )
        ]
        
        return mock_results[:max_results]

class WebBrowserTool:
    """Web page content extraction and browsing"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.timeout = 10
    
    def fetch_page(self, url: str) -> Optional[WebPageContent]:
        """Fetch and parse a web page"""
        
        try:
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            
            # Basic HTML parsing (would use BeautifulSoup in production)
            content = self._extract_text_content(response.text)
            title = self._extract_title(response.text)
            links = self._extract_links(response.text, url)
            
            return WebPageContent(
                url=url,
                title=title,
                content=content,
                links=links,
                metadata={
                    "status_code": response.status_code,
                    "content_type": response.headers.get("content-type", ""),
                    "content_length": len(response.text)
                }
            )
            
        except Exception as e:
            # Return mock content for demo
            return self._mock_page_content(url)
    
    def _extract_text_content(self, html: str) -> str:
        """Extract text content from HTML (basic implementation)"""
        
        # Remove script and style elements
        html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL | re.IGNORECASE)
        html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL | re.IGNORECASE)
        
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', '', html)
        
        # Clean up whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Limit content length
        return text[:5000] if len(text) > 5000 else text
    
    def _extract_title(self, html: str) -> str:
        """Extract page title from HTML"""
        
        title_match = re.search(r'<title[^>]*>(.*?)</title>', html, re.IGNORECASE | re.DOTALL)
        if title_match:
            return title_match.group(1).strip()
        return "Untitled Page"
    
    def _extract_links(self, html: str, base_url: str) -> List[str]:
        """Extract links from HTML"""
        
        links = []
        link_pattern = r'<a[^>]+href=["\']([^"\']+)["\'][^>]*>'
        
        for match in re.finditer(link_pattern, html, re.IGNORECASE):
            href = match.group(1)
            
            # Convert relative URLs to absolute
            if href.startswith('http'):
                links.append(href)
            elif href.startswith('/'):
                links.append(urljoin(base_url, href))
        
        return links[:20]  # Limit number of links
    
    def _mock_page_content(self, url: str) -> WebPageContent:
        """Generate mock page content for demonstration"""
        
        domain = urlparse(url).netloc or "example.com"
        
        return WebPageContent(
            url=url,
            title=f"Page from {domain}",
            content=f"This is mock content from {url}. In a real implementation, this would contain the actual page content extracted from the HTML.",
            links=[
                f"https://{domain}/page1",
                f"https://{domain}/page2",
                f"https://{domain}/about"
            ],
            metadata={
                "status_code": 200,
                "content_type": "text/html",
                "content_length": 1000
            }
        )

class WebResearchTool:
    """High-level web research combining search and browsing"""
    
    def __init__(self):
        self.search_tool = WebSearchTool()
        self.browser_tool = WebBrowserTool()
    
    def research_topic(self, topic: str, depth: int = 3) -> Dict[str, Any]:
        """Research a topic by searching and analyzing multiple sources"""
        
        research_results = {
            "topic": topic,
            "search_results": [],
            "page_contents": [],
            "summary": "",
            "key_points": [],
            "sources": []
        }
        
        try:
            # Step 1: Search for information
            search_results = self.search_tool.search(topic, max_results=depth)
            research_results["search_results"] = [
                {
                    "title": result.title,
                    "url": result.url,
                    "snippet": result.snippet,
                    "relevance": result.relevance_score
                }
                for result in search_results
            ]
            
            # Step 2: Fetch content from top results
            for result in search_results[:min(depth, 3)]:  # Limit to avoid too many requests
                page_content = self.browser_tool.fetch_page(result.url)
                if page_content:
                    research_results["page_contents"].append({
                        "url": page_content.url,
                        "title": page_content.title,
                        "content": page_content.content[:1000],  # Truncate for summary
                        "links_count": len(page_content.links)
                    })
                    research_results["sources"].append(result.url)
            
            # Step 3: Generate summary and key points
            research_results["summary"] = self._generate_summary(research_results)
            research_results["key_points"] = self._extract_key_points(research_results)
            
        except Exception as e:
            research_results["error"] = str(e)
            research_results["summary"] = f"Unable to complete research on {topic} due to technical issues."
        
        return research_results
    
    def _generate_summary(self, research_data: Dict[str, Any]) -> str:
        """Generate a summary from research data"""
        
        topic = research_data["topic"]
        sources_count = len(research_data["sources"])
        
        if sources_count == 0:
            return f"No reliable sources found for {topic}."
        
        # Basic summary generation (would use LLM in production)
        summary = f"Research on {topic} was conducted using {sources_count} sources. "
        
        if research_data["page_contents"]:
            summary += "Key information was gathered from multiple web pages including "
            titles = [content["title"] for content in research_data["page_contents"]]
            summary += ", ".join(titles[:2])
            if len(titles) > 2:
                summary += f" and {len(titles) - 2} other sources"
            summary += "."
        
        return summary
    
    def _extract_key_points(self, research_data: Dict[str, Any]) -> List[str]:
        """Extract key points from research data"""
        
        key_points = []
        
        # Extract from search snippets
        for result in research_data["search_results"]:
            if len(result["snippet"]) > 50:
                key_points.append(result["snippet"][:200] + "...")
        
        # Extract from page contents (basic implementation)
        for content in research_data["page_contents"]:
            sentences = content["content"].split('. ')
            for sentence in sentences[:2]:  # First 2 sentences
                if len(sentence) > 30:
                    key_points.append(sentence.strip() + ".")
        
        return key_points[:5]  # Limit to top 5 key points
    
    def verify_information(self, claim: str, sources: List[str] = None) -> Dict[str, Any]:
        """Verify information against multiple sources"""
        
        verification_result = {
            "claim": claim,
            "verification_status": "unknown",
            "confidence": 0.0,
            "supporting_sources": [],
            "contradicting_sources": [],
            "analysis": ""
        }
        
        try:
            # Search for information about the claim
            search_query = f"verify {claim}"
            search_results = self.search_tool.search(search_query, max_results=5)
            
            # Analyze search results (basic implementation)
            supporting_count = 0
            contradicting_count = 0
            
            for result in search_results:
                snippet_lower = result.snippet.lower()
                claim_lower = claim.lower()
                
                # Simple keyword matching (would use NLP in production)
                if any(word in snippet_lower for word in claim_lower.split()):
                    if any(word in snippet_lower for word in ["true", "correct", "confirmed", "verified"]):
                        supporting_count += 1
                        verification_result["supporting_sources"].append(result.url)
                    elif any(word in snippet_lower for word in ["false", "incorrect", "debunked", "myth"]):
                        contradicting_count += 1
                        verification_result["contradicting_sources"].append(result.url)
            
            # Determine verification status
            if supporting_count > contradicting_count:
                verification_result["verification_status"] = "likely_true"
                verification_result["confidence"] = min(0.8, supporting_count * 0.2)
            elif contradicting_count > supporting_count:
                verification_result["verification_status"] = "likely_false"
                verification_result["confidence"] = min(0.8, contradicting_count * 0.2)
            else:
                verification_result["verification_status"] = "inconclusive"
                verification_result["confidence"] = 0.3
            
            verification_result["analysis"] = f"Found {supporting_count} supporting and {contradicting_count} contradicting sources."
            
        except Exception as e:
            verification_result["analysis"] = f"Unable to verify claim due to technical issues: {str(e)}"
        
        return verification_result