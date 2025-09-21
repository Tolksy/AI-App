"""
Real Web Scraping Agent - Actually scrapes websites for lead generation
"""

import asyncio
import aiohttp
import logging
from typing import List, Dict, Any, Optional
from bs4 import BeautifulSoup
import re
import time
from urllib.parse import urljoin, urlparse
from agent_tasks import TaskTracker, TaskType, task_tracker

logger = logging.getLogger(__name__)

class WebScrapingAgent:
    def __init__(self):
        self.session = None
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession(headers=self.headers)
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def scrape_website(self, url: str, search_terms: List[str] = None) -> Dict[str, Any]:
        """Scrape a website for lead generation information"""
        task = task_tracker.create_task(
            TaskType.WEB_SCRAPING,
            f"Scraping website: {url}",
            {"url": url, "search_terms": search_terms}
        )
        
        try:
            task_tracker.start_task(task.id)
            
            async with self.session.get(url) as response:
                if response.status == 200:
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    # Extract basic information
                    title = soup.find('title').get_text() if soup.find('title') else "No title"
                    
                    # Look for contact information
                    contact_info = self._extract_contact_info(soup)
                    
                    # Look for business information
                    business_info = self._extract_business_info(soup, search_terms)
                    
                    # Look for social media links
                    social_links = self._extract_social_links(soup)
                    
                    result = {
                        "url": url,
                        "title": title,
                        "contact_info": contact_info,
                        "business_info": business_info,
                        "social_links": social_links,
                        "scraped_at": time.time(),
                        "status": "success"
                    }
                    
                    task_tracker.complete_task(task.id, result)
                    return result
                else:
                    error_msg = f"HTTP {response.status}: {response.reason}"
                    task_tracker.fail_task(task.id, error_msg)
                    return {"status": "error", "error": error_msg}
        
        except Exception as e:
            error_msg = f"Scraping error: {str(e)}"
            task_tracker.fail_task(task.id, error_msg)
            logger.error(error_msg)
            return {"status": "error", "error": error_msg}
    
    def _extract_contact_info(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Extract contact information from webpage"""
        contact_info = {
            "emails": [],
            "phones": [],
            "addresses": []
        }
        
        # Find emails
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        text = soup.get_text()
        emails = re.findall(email_pattern, text)
        contact_info["emails"] = list(set(emails))
        
        # Find phone numbers
        phone_pattern = r'(\+?1?[-.\s]?)?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})'
        phones = re.findall(phone_pattern, text)
        contact_info["phones"] = [''.join(phone) for phone in phones[:5]]  # Limit to 5
        
        # Look for contact sections
        contact_sections = soup.find_all(['div', 'section'], class_=re.compile(r'contact|address|location', re.I))
        for section in contact_sections:
            addresses = self._extract_addresses(section.get_text())
            contact_info["addresses"].extend(addresses)
        
        return contact_info
    
    def _extract_business_info(self, soup: BeautifulSoup, search_terms: List[str] = None) -> Dict[str, Any]:
        """Extract business information relevant to search terms"""
        business_info = {
            "description": "",
            "services": [],
            "industry_keywords": [],
            "company_size": "",
            "location": ""
        }
        
        # Get meta description
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc:
            business_info["description"] = meta_desc.get('content', '')
        
        # Look for services or products
        service_keywords = ['services', 'products', 'solutions', 'offerings']
        for keyword in service_keywords:
            service_section = soup.find(['div', 'section'], class_=re.compile(keyword, re.I))
            if service_section:
                services = service_section.find_all(['li', 'p'])
                business_info["services"] = [s.get_text().strip() for s in services[:10]]
                break
        
        # Extract industry keywords if search terms provided
        if search_terms:
            text = soup.get_text().lower()
            found_keywords = [term for term in search_terms if term.lower() in text]
            business_info["industry_keywords"] = found_keywords
        
        return business_info
    
    def _extract_social_links(self, soup: BeautifulSoup) -> Dict[str, str]:
        """Extract social media links"""
        social_links = {}
        social_platforms = {
            'linkedin': 'linkedin.com',
            'twitter': 'twitter.com',
            'facebook': 'facebook.com',
            'instagram': 'instagram.com',
            'youtube': 'youtube.com'
        }
        
        for platform, domain in social_platforms.items():
            link = soup.find('a', href=re.compile(domain, re.I))
            if link:
                social_links[platform] = link.get('href')
        
        return social_links
    
    def _extract_addresses(self, text: str) -> List[str]:
        """Extract potential addresses from text"""
        # Simple address pattern (can be improved)
        address_pattern = r'\d+\s+[A-Za-z0-9\s,.-]+(?:Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd|Drive|Dr|Lane|Ln)'
        addresses = re.findall(address_pattern, text, re.I)
        return addresses[:3]  # Limit to 3 addresses
    
    async def scrape_multiple_sites(self, urls: List[str], search_terms: List[str] = None) -> List[Dict[str, Any]]:
        """Scrape multiple websites concurrently"""
        task = task_tracker.create_task(
            TaskType.WEB_SCRAPING,
            f"Scraping {len(urls)} websites",
            {"urls": urls, "search_terms": search_terms}
        )
        
        try:
            task_tracker.start_task(task.id)
            results = []
            
            # Process URLs in batches to avoid overwhelming servers
            batch_size = 5
            for i in range(0, len(urls), batch_size):
                batch = urls[i:i + batch_size]
                batch_results = await asyncio.gather(
                    *[self.scrape_website(url, search_terms) for url in batch],
                    return_exceptions=True
                )
                
                for result in batch_results:
                    if isinstance(result, dict):
                        results.append(result)
                
                # Update progress
                progress = int((i + batch_size) / len(urls) * 100)
                task_tracker.update_task_progress(task.id, progress)
                
                # Small delay between batches
                await asyncio.sleep(1)
            
            task_tracker.complete_task(task.id, {"results": results, "total_scraped": len(results)})
            return results
        
        except Exception as e:
            error_msg = f"Batch scraping error: {str(e)}"
            task_tracker.fail_task(task.id, error_msg)
            logger.error(error_msg)
            return []

class LeadResearchAgent:
    def __init__(self):
        self.scraper = WebScrapingAgent()
    
    async def research_company(self, company_name: str, industry: str = None) -> Dict[str, Any]:
        """Research a specific company for lead generation"""
        task = task_tracker.create_task(
            TaskType.LEAD_QUALIFICATION,
            f"Researching company: {company_name}",
            {"company_name": company_name, "industry": industry}
        )
        
        try:
            task_tracker.start_task(task.id)
            
            # Generate potential URLs to search
            search_urls = [
                f"https://www.{company_name.lower().replace(' ', '')}.com",
                f"https://{company_name.lower().replace(' ', '')}.com",
                f"https://www.{company_name.lower().replace(' ', '')}.net",
                f"https://{company_name.lower().replace(' ', '')}.net"
            ]
            
            results = []
            async with self.scraper as scraper:
                for url in search_urls:
                    try:
                        result = await scraper.scrape_website(url, [industry] if industry else None)
                        if result.get("status") == "success":
                            results.append(result)
                            break  # Found working site, stop searching
                    except Exception as e:
                        logger.warning(f"Failed to scrape {url}: {str(e)}")
                        continue
            
            if results:
                company_data = results[0]
                company_data["research_type"] = "company_research"
                company_data["industry"] = industry
                company_data["lead_score"] = self._calculate_lead_score(company_data)
                
                task_tracker.complete_task(task.id, company_data)
                return company_data
            else:
                error_msg = f"No accessible website found for {company_name}"
                task_tracker.fail_task(task.id, error_msg)
                return {"status": "error", "error": error_msg}
        
        except Exception as e:
            error_msg = f"Company research error: {str(e)}"
            task_tracker.fail_task(task.id, error_msg)
            logger.error(error_msg)
            return {"status": "error", "error": error_msg}
    
    def _calculate_lead_score(self, company_data: Dict[str, Any]) -> int:
        """Calculate a lead score based on available information"""
        score = 0
        
        # Contact information availability
        if company_data.get("contact_info", {}).get("emails"):
            score += 30
        if company_data.get("contact_info", {}).get("phones"):
            score += 20
        if company_data.get("contact_info", {}).get("addresses"):
            score += 15
        
        # Business information quality
        if company_data.get("business_info", {}).get("description"):
            score += 20
        if company_data.get("business_info", {}).get("services"):
            score += 15
        
        # Social media presence
        social_links = company_data.get("social_links", {})
        score += len(social_links) * 5
        
        return min(100, score)  # Cap at 100
