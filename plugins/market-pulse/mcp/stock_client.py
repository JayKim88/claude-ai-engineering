"""
Stock MCP Client
MCP 서버와 통신하는 클라이언트 래퍼
"""

import subprocess
import json
import os
from typing import Dict, Optional


class StockMCPClient:
    """
    Stock MCP 서버와 통신하는 클라이언트
    Python 코드에서 쉽게 사용할 수 있도록 래핑
    """

    def __init__(self, server_path: Optional[str] = None):
        """
        Args:
            server_path: MCP 서버 스크립트 경로 (기본값: 현재 디렉토리의 stock_mcp_server.py)
        """
        if server_path is None:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            server_path = os.path.join(current_dir, "stock_mcp_server.py")

        self.server_path = server_path
        self.request_id = 0

    def _send_request(self, method: str, params: Optional[Dict] = None) -> Dict:
        """MCP 서버에 요청 전송"""
        self.request_id += 1

        request = {
            "jsonrpc": "2.0",
            "id": self.request_id,
            "method": method,
            "params": params or {}
        }

        try:
            # MCP 서버 프로세스 시작
            process = subprocess.Popen(
                ["python3", self.server_path],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            # 요청 전송
            stdout, stderr = process.communicate(
                input=json.dumps(request) + "\n",
                timeout=10
            )

            if stderr:
                print(f"Warning: {stderr}")

            # 응답 파싱
            if stdout.strip():
                response = json.loads(stdout.strip().split('\n')[-1])
                if "error" in response:
                    raise Exception(f"MCP Error: {response['error']}")
                return response.get("result", {})

            return {}

        except subprocess.TimeoutExpired:
            process.kill()
            raise Exception("MCP server timeout")
        except Exception as e:
            raise Exception(f"MCP client error: {str(e)}")

    def get_fundamental_metrics(self, ticker: str) -> Dict:
        """펀더멘털 지표 조회"""
        result = self._send_request(
            "tools/call",
            {
                "name": "get_fundamental_metrics",
                "arguments": {"ticker": ticker}
            }
        )

        # content에서 실제 데이터 추출
        if "content" in result and len(result["content"]) > 0:
            text = result["content"][0].get("text", "{}")
            return json.loads(text)

        return result

    def get_valuation_metrics(self, ticker: str) -> Dict:
        """밸류에이션 지표"""
        result = self._send_request(
            "tools/call",
            {
                "name": "get_valuation_metrics",
                "arguments": {"ticker": ticker}
            }
        )

        if "content" in result and len(result["content"]) > 0:
            text = result["content"][0].get("text", "{}")
            return json.loads(text)

        return result

    def get_profitability_metrics(self, ticker: str) -> Dict:
        """수익성 지표"""
        result = self._send_request(
            "tools/call",
            {
                "name": "get_profitability_metrics",
                "arguments": {"ticker": ticker}
            }
        )

        if "content" in result and len(result["content"]) > 0:
            text = result["content"][0].get("text", "{}")
            return json.loads(text)

        return result

    def get_growth_metrics(self, ticker: str) -> Dict:
        """성장률 지표"""
        result = self._send_request(
            "tools/call",
            {
                "name": "get_growth_metrics",
                "arguments": {"ticker": ticker}
            }
        )

        if "content" in result and len(result["content"]) > 0:
            text = result["content"][0].get("text", "{}")
            return json.loads(text)

        return result

    def get_financial_health(self, ticker: str) -> Dict:
        """재무 건전성"""
        result = self._send_request(
            "tools/call",
            {
                "name": "get_financial_health",
                "arguments": {"ticker": ticker}
            }
        )

        if "content" in result and len(result["content"]) > 0:
            text = result["content"][0].get("text", "{}")
            return json.loads(text)

        return result

    def get_dividend_info(self, ticker: str) -> Dict:
        """배당 정보"""
        result = self._send_request(
            "tools/call",
            {
                "name": "get_dividend_info",
                "arguments": {"ticker": ticker}
            }
        )

        if "content" in result and len(result["content"]) > 0:
            text = result["content"][0].get("text", "{}")
            return json.loads(text)

        return result

    def get_company_info(self, ticker: str) -> Dict:
        """기업 기본 정보"""
        result = self._send_request(
            "tools/call",
            {
                "name": "get_company_info",
                "arguments": {"ticker": ticker}
            }
        )

        if "content" in result and len(result["content"]) > 0:
            text = result["content"][0].get("text", "{}")
            return json.loads(text)

        return result

    def get_price_data(self, ticker: str) -> Dict:
        """가격 데이터"""
        result = self._send_request(
            "tools/call",
            {
                "name": "get_price_data",
                "arguments": {"ticker": ticker}
            }
        )

        if "content" in result and len(result["content"]) > 0:
            text = result["content"][0].get("text", "{}")
            return json.loads(text)

        return result

    def get_all_metrics(self, ticker: str) -> Dict:
        """모든 지표 종합"""
        result = self._send_request(
            "tools/call",
            {
                "name": "get_all_metrics",
                "arguments": {"ticker": ticker}
            }
        )

        if "content" in result and len(result["content"]) > 0:
            text = result["content"][0].get("text", "{}")
            return json.loads(text)

        return result


# 사용 예시
if __name__ == "__main__":
    client = StockMCPClient()

    # AAPL 펀더멘털 조회
    print("=== Apple 펀더멘털 지표 ===")
    metrics = client.get_fundamental_metrics("AAPL")
    print(json.dumps(metrics, indent=2, ensure_ascii=False))

    print("\n=== Apple 밸류에이션 ===")
    valuation = client.get_valuation_metrics("AAPL")
    print(json.dumps(valuation, indent=2, ensure_ascii=False))
