import requests
from requests.exceptions import RequestException, SSLError, ConnectionError
from urllib3.exceptions import InsecureRequestWarning
import logging
from typing import Optional, Union, Dict

class WebRequestHandler:
    def __init__(self, verify_ssl: bool = False):
        """
        웹 요청 핸들러 초기화
        
        Args:
            verify_ssl (bool): SSL 인증서 검증 여부
        """
        self.verify_ssl = verify_ssl
        
        # SSL 경고 메시지 비활성화 (verify_ssl이 False일 때)
        if not verify_ssl:
            requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        
        # 로깅 설정
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

            # log를 파일에 출력
            file_handler = logging.FileHandler('web_check.log')
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

    def get_url_content(self, url: str, timeout: int = 3) -> Optional[str]:
        """
        URL로부터 컨텐츠를 안전하게 가져오기
        
        Args:
            url (str): 요청할 URL
            timeout (int): 요청 타임아웃 시간(초)
            
        Returns:
            Optional[str]: 성공 시 컨텐츠, 실패 시 None
        """
        try:
            response = requests.get(
                url,
                verify=self.verify_ssl,
                timeout=timeout
            )
            response.raise_for_status()
            self.logger.info("Usable URL!")
            return "Usable"
            
        except SSLError as e:
            self.logger.warning(f"SSL 인증서 오류 - {url}: {str(e)}")
            return "Unusable"
            
        except ConnectionError as e:
            self.logger.warning(f"연결 오류 (도메인 접근 불가) - {url}: {str(e)}")
            return "Unusable"
            
        except requests.exceptions.HTTPError as e:
            self.logger.warning(f"HTTP 오류 - {url}: {str(e)}")
            return "Unusable"
            
        except requests.exceptions.Timeout as e:
            self.logger.warning(f"타임아웃 - {url}: {str(e)}")
            return "Unusable"
            
        except RequestException as e:
            self.logger.warning(f"요청 실패 - {url}: {str(e)}")
            return "Unusable"
            
        except Exception as e:
            self.logger.error(f"예상치 못한 오류 - {url}: {str(e)}")
            return "Unusable"

def process_multiple_urls(urls: list) -> Dict[str, Optional[str]]:
    """
    여러 URL을 처리하고 결과를 반환
    
    Args:
        urls (list): 처리할 URL 리스트
        
    Returns:
        Dict[str, Optional[str]]: URL별 처리 결과
    """
    handler = WebRequestHandler(verify_ssl=False)
    results = {}
    
    for i, url in enumerate(urls, 1):
        
        print(f"Current count : {i}/{len(urls)}")
        
        content = handler.get_url_content(url)
        results[url] = content
        
    return results

# 사용 예시
if __name__ == "__main__":
    # 테스트할 URL 리스트
    test_urls = [
        "https://www.moguchon.co.kr/wn/",
        "https://flip.dorelan.co.kr",
        "https://www.google.com"
    ]
    
    # 결과 처리
    results = process_multiple_urls(test_urls)
    print(results)
    
    # 결과 출력
    for url, content in results.items():
        if content:
            print(f"성공: {url}, {content}")
        else:
            print(f"실패: {url}, {content}")