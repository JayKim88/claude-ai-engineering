"""
Technical Indicators Calculator
Calculates and interprets technical indicators for market analysis.
"""

import pandas as pd
import numpy as np
from typing import Dict, Tuple, Optional, List

try:
    import pandas_ta as ta
    PANDAS_TA_AVAILABLE = True
except ImportError:
    PANDAS_TA_AVAILABLE = False
    print("⚠️  pandas-ta not available, using manual calculations")


class TechnicalIndicatorCalculator:
    """
    Calculate and interpret technical indicators for stocks/ETFs.

    Supported Indicators:
    - RSI (Relative Strength Index)
    - MACD (Moving Average Convergence Divergence)
    - SMA/EMA (Simple/Exponential Moving Averages)
    - Bollinger Bands
    - ATR (Average True Range)
    - OBV (On-Balance Volume)
    """

    def __init__(self):
        """Initialize calculator."""
        self.use_pandas_ta = PANDAS_TA_AVAILABLE

    # ========== RSI ==========

    def calculate_rsi(self, prices: pd.Series, period: int = 14) -> pd.Series:
        """
        Calculate Relative Strength Index (RSI).

        Args:
            prices: Series of closing prices
            period: RSI period (default: 14)

        Returns:
            Series of RSI values (0-100)
        """
        if self.use_pandas_ta:
            try:
                return ta.rsi(prices, length=period)
            except Exception as e:
                print(f"pandas-ta RSI failed: {e}, using manual calculation")

        # Manual RSI calculation
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()

        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))

        return rsi

    def interpret_rsi(self, rsi_value: float) -> Tuple[str, str, str]:
        """
        Interpret RSI value with beginner-friendly explanation.

        Args:
            rsi_value: RSI value (0-100)

        Returns:
            Tuple of (interpretation, color, explanation_ko)
        """
        if pd.isna(rsi_value):
            return ("데이터 부족", "gray", "RSI 계산을 위한 데이터가 부족합니다.")

        if rsi_value >= 70:
            return (
                "과매수 (조정 가능성)",
                "red",
                f"RSI {rsi_value:.1f}은 과매수 영역입니다. 단기 조정이 올 수 있으니 신규 매수는 신중하게 접근하세요."
            )
        elif rsi_value >= 60:
            return (
                "상승 추세 (강세)",
                "orange",
                f"RSI {rsi_value:.1f}은 강한 상승 추세를 나타냅니다. 과매수 영역 근접에 주의하세요."
            )
        elif rsi_value >= 40:
            return (
                "중립 (관망)",
                "gray",
                f"RSI {rsi_value:.1f}은 중립 영역입니다. 명확한 신호가 없으니 다른 지표와 함께 판단하세요."
            )
        elif rsi_value >= 30:
            return (
                "하락 추세 (약세)",
                "yellow",
                f"RSI {rsi_value:.1f}은 약한 하락 추세입니다. 과매도 영역 근접에 반등 기회를 모니터링하세요."
            )
        else:
            return (
                "과매도 (반등 기회)",
                "green",
                f"RSI {rsi_value:.1f}은 과매도 영역입니다. 반등 기회가 올 수 있으나, 추가 하락 위험도 있으니 신중하게 접근하세요."
            )

    # ========== MACD ==========

    def calculate_macd(
        self,
        prices: pd.Series,
        fast: int = 12,
        slow: int = 26,
        signal: int = 9
    ) -> Dict[str, pd.Series]:
        """
        Calculate MACD (Moving Average Convergence Divergence).

        Args:
            prices: Series of closing prices
            fast: Fast EMA period (default: 12)
            slow: Slow EMA period (default: 26)
            signal: Signal line period (default: 9)

        Returns:
            Dictionary with keys: macd, signal, histogram
        """
        if self.use_pandas_ta:
            try:
                macd_result = ta.macd(prices, fast=fast, slow=slow, signal=signal)
                return {
                    'macd': macd_result[f'MACD_{fast}_{slow}_{signal}'],
                    'signal': macd_result[f'MACDs_{fast}_{slow}_{signal}'],
                    'histogram': macd_result[f'MACDh_{fast}_{slow}_{signal}']
                }
            except Exception as e:
                print(f"pandas-ta MACD failed: {e}, using manual calculation")

        # Manual MACD calculation
        ema_fast = prices.ewm(span=fast, adjust=False).mean()
        ema_slow = prices.ewm(span=slow, adjust=False).mean()
        macd = ema_fast - ema_slow
        signal_line = macd.ewm(span=signal, adjust=False).mean()
        histogram = macd - signal_line

        return {
            'macd': macd,
            'signal': signal_line,
            'histogram': histogram
        }

    def interpret_macd(
        self,
        macd: float,
        signal: float,
        histogram: float,
        prev_histogram: float = None
    ) -> Tuple[str, str, str]:
        """
        Interpret MACD values.

        Args:
            macd: MACD line value
            signal: Signal line value
            histogram: MACD histogram
            prev_histogram: Previous histogram value (for crossover detection)

        Returns:
            Tuple of (interpretation, color, explanation_ko)
        """
        if pd.isna(macd) or pd.isna(signal):
            return ("데이터 부족", "gray", "MACD 계산을 위한 데이터가 부족합니다.")

        # Detect crossovers
        if prev_histogram is not None:
            if prev_histogram < 0 and histogram > 0:
                return (
                    "골든 크로스 (매수 신호)",
                    "green",
                    "MACD가 시그널선을 상향 돌파했습니다. 상승 추세 전환 신호로 매수 타이밍으로 고려할 수 있습니다."
                )
            elif prev_histogram > 0 and histogram < 0:
                return (
                    "데드 크로스 (매도 신호)",
                    "red",
                    "MACD가 시그널선을 하향 돌파했습니다. 하락 추세 전환 신호로 매도 또는 관망을 고려하세요."
                )

        # General interpretation
        if histogram > 0:
            strength = "강한" if abs(histogram) > 5 else "약한"
            return (
                f"{strength} 상승 추세",
                "green" if abs(histogram) > 5 else "lightgreen",
                f"MACD({macd:.2f})가 시그널({signal:.2f})보다 위에 있습니다. {strength} 상승 추세입니다."
            )
        else:
            strength = "강한" if abs(histogram) > 5 else "약한"
            return (
                f"{strength} 하락 추세",
                "red" if abs(histogram) > 5 else "pink",
                f"MACD({macd:.2f})가 시그널({signal:.2f})보다 아래에 있습니다. {strength} 하락 추세입니다."
            )

    # ========== Moving Averages ==========

    def calculate_sma(self, prices: pd.Series, period: int) -> pd.Series:
        """Calculate Simple Moving Average."""
        if self.use_pandas_ta:
            try:
                return ta.sma(prices, length=period)
            except:
                pass

        return prices.rolling(window=period).mean()

    def calculate_ema(self, prices: pd.Series, period: int) -> pd.Series:
        """Calculate Exponential Moving Average."""
        if self.use_pandas_ta:
            try:
                return ta.ema(prices, length=period)
            except:
                pass

        return prices.ewm(span=period, adjust=False).mean()

    def interpret_moving_averages(
        self,
        price: float,
        sma_20: float,
        sma_50: float,
        sma_200: float
    ) -> Tuple[str, str, str]:
        """
        Interpret moving average alignment.

        Args:
            price: Current price
            sma_20: 20-day SMA
            sma_50: 50-day SMA
            sma_200: 200-day SMA

        Returns:
            Tuple of (trend, color, explanation_ko)
        """
        # Check for golden cross (50 > 200) or death cross (50 < 200)
        if pd.notna(sma_50) and pd.notna(sma_200):
            if sma_50 > sma_200 and price > sma_50:
                return (
                    "강한 상승 추세 (골든 크로스)",
                    "green",
                    f"50일선({sma_50:.2f})이 200일선({sma_200:.2f})보다 위에 있고, 현재가({price:.2f})도 상승 중입니다. 강한 상승 추세입니다."
                )
            elif sma_50 < sma_200 and price < sma_50:
                return (
                    "강한 하락 추세 (데드 크로스)",
                    "red",
                    f"50일선({sma_50:.2f})이 200일선({sma_200:.2f})보다 아래에 있고, 현재가({price:.2f})도 하락 중입니다. 강한 하락 추세입니다."
                )

        # Simple alignment check
        if price > sma_20 > sma_50:
            return ("상승 추세", "green", f"가격이 이동평균선들 위에 있습니다. 상승 추세입니다.")
        elif price < sma_20 < sma_50:
            return ("하락 추세", "red", f"가격이 이동평균선들 아래에 있습니다. 하락 추세입니다.")
        else:
            return ("혼조세 (방향성 불명확)", "gray", "이동평균선이 뒤섞여 있습니다. 명확한 추세가 없습니다.")

    # ========== Bollinger Bands ==========

    def calculate_bollinger_bands(
        self,
        prices: pd.Series,
        period: int = 20,
        std_dev: float = 2.0
    ) -> Dict[str, pd.Series]:
        """
        Calculate Bollinger Bands.

        Args:
            prices: Series of closing prices
            period: MA period (default: 20)
            std_dev: Standard deviation multiplier (default: 2.0)

        Returns:
            Dictionary with keys: upper, middle, lower
        """
        if self.use_pandas_ta:
            try:
                bb_result = ta.bbands(prices, length=period, std=std_dev)
                return {
                    'upper': bb_result[f'BBU_{period}_{std_dev}'],
                    'middle': bb_result[f'BBM_{period}_{std_dev}'],
                    'lower': bb_result[f'BBL_{period}_{std_dev}']
                }
            except:
                pass

        # Manual calculation
        middle = prices.rolling(window=period).mean()
        std = prices.rolling(window=period).std()
        upper = middle + (std * std_dev)
        lower = middle - (std * std_dev)

        return {
            'upper': upper,
            'middle': middle,
            'lower': lower
        }

    def interpret_bollinger_bands(
        self,
        price: float,
        upper: float,
        middle: float,
        lower: float
    ) -> Tuple[str, str, str]:
        """Interpret Bollinger Bands position."""
        if pd.isna(upper) or pd.isna(lower):
            return ("데이터 부족", "gray", "볼린저 밴드 계산 데이터 부족")

        band_width = upper - lower
        position = (price - lower) / band_width if band_width > 0 else 0.5

        if position >= 0.9:
            return (
                "과매수 (상단 밴드 근접)",
                "red",
                f"가격({price:.2f})이 볼린저 밴드 상단({upper:.2f}) 근처입니다. 과매수 상태로 조정 가능성이 있습니다."
            )
        elif position <= 0.1:
            return (
                "과매도 (하단 밴드 근접)",
                "green",
                f"가격({price:.2f})이 볼린저 밴드 하단({lower:.2f}) 근처입니다. 과매도 상태로 반등 기회가 있을 수 있습니다."
            )
        else:
            return (
                "정상 범위",
                "gray",
                f"가격({price:.2f})이 볼린저 밴드 중간({middle:.2f}) 근처에서 거래 중입니다."
            )

    # ========== Comprehensive Analysis ==========

    def analyze_stock(
        self,
        df: pd.DataFrame,
        price_column: str = 'close'
    ) -> Dict[str, any]:
        """
        Perform comprehensive technical analysis on a stock.

        Args:
            df: DataFrame with OHLCV data (columns: date, open, high, low, close, volume)
            price_column: Column name for closing prices (default: 'close')

        Returns:
            Dictionary with all indicators and interpretations
        """
        prices = df[price_column]
        latest_price = prices.iloc[-1]

        # Calculate all indicators
        rsi = self.calculate_rsi(prices)
        macd_data = self.calculate_macd(prices)
        sma_20 = self.calculate_sma(prices, 20)
        sma_50 = self.calculate_sma(prices, 50)
        sma_200 = self.calculate_sma(prices, 200)
        ema_12 = self.calculate_ema(prices, 12)
        ema_26 = self.calculate_ema(prices, 26)
        bb = self.calculate_bollinger_bands(prices)

        # Get latest values
        latest_rsi = rsi.iloc[-1]
        latest_macd = macd_data['macd'].iloc[-1]
        latest_signal = macd_data['signal'].iloc[-1]
        latest_histogram = macd_data['histogram'].iloc[-1]
        prev_histogram = macd_data['histogram'].iloc[-2] if len(macd_data['histogram']) > 1 else None

        # Interpretations
        rsi_interp = self.interpret_rsi(latest_rsi)
        macd_interp = self.interpret_macd(latest_macd, latest_signal, latest_histogram, prev_histogram)

        # Safe extraction of SMA values
        sma_20_val = sma_20.iloc[-1] if sma_20 is not None and len(sma_20) > 0 else None
        sma_50_val = sma_50.iloc[-1] if sma_50 is not None and len(sma_50) >= 50 else None
        sma_200_val = sma_200.iloc[-1] if sma_200 is not None and len(sma_200) >= 200 else None

        ma_interp = self.interpret_moving_averages(
            latest_price,
            sma_20_val,
            sma_50_val,
            sma_200_val
        )
        bb_interp = self.interpret_bollinger_bands(
            latest_price,
            bb['upper'].iloc[-1],
            bb['middle'].iloc[-1],
            bb['lower'].iloc[-1]
        )

        return {
            'price': latest_price,
            'indicators': {
                'rsi': latest_rsi,
                'macd': latest_macd,
                'macd_signal': latest_signal,
                'macd_histogram': latest_histogram,
                'sma_20': sma_20_val,
                'sma_50': sma_50_val,
                'sma_200': sma_200_val,
                'bb_upper': bb['upper'].iloc[-1],
                'bb_middle': bb['middle'].iloc[-1],
                'bb_lower': bb['lower'].iloc[-1]
            },
            'interpretations': {
                'rsi': {
                    'label': rsi_interp[0],
                    'color': rsi_interp[1],
                    'explanation': rsi_interp[2]
                },
                'macd': {
                    'label': macd_interp[0],
                    'color': macd_interp[1],
                    'explanation': macd_interp[2]
                },
                'moving_averages': {
                    'label': ma_interp[0],
                    'color': ma_interp[1],
                    'explanation': ma_interp[2]
                },
                'bollinger_bands': {
                    'label': bb_interp[0],
                    'color': bb_interp[1],
                    'explanation': bb_interp[2]
                }
            },
            'series': {
                'rsi': rsi,
                'macd': macd_data['macd'],
                'macd_signal': macd_data['signal'],
                'sma_20': sma_20,
                'sma_50': sma_50,
                'sma_200': sma_200,
                'bb_upper': bb['upper'],
                'bb_middle': bb['middle'],
                'bb_lower': bb['lower']
            }
        }


# Convenience function
def get_calculator() -> TechnicalIndicatorCalculator:
    """Get a TechnicalIndicatorCalculator instance."""
    return TechnicalIndicatorCalculator()


if __name__ == "__main__":
    # Test with sample data
    print("Testing TechnicalIndicatorCalculator...")

    # Create sample price data
    dates = pd.date_range('2025-08-01', periods=60, freq='D')
    prices = pd.Series([100 + i * 0.5 + np.random.randn() * 2 for i in range(60)], index=dates)

    df = pd.DataFrame({
        'date': dates,
        'close': prices,
        'open': prices - 0.5,
        'high': prices + 1,
        'low': prices - 1,
        'volume': [1000000] * 60
    })

    calc = TechnicalIndicatorCalculator()
    analysis = calc.analyze_stock(df)

    print(f"\n📊 Analysis Results:")
    print(f"Price: ${analysis['price']:.2f}")
    print(f"\nRSI: {analysis['indicators']['rsi']:.1f}")
    print(f"  → {analysis['interpretations']['rsi']['label']}")
    print(f"  → {analysis['interpretations']['rsi']['explanation']}")

    print(f"\nMACD: {analysis['indicators']['macd']:.2f}")
    print(f"  → {analysis['interpretations']['macd']['label']}")
    print(f"  → {analysis['interpretations']['macd']['explanation']}")

    print(f"\n이동평균: {analysis['interpretations']['moving_averages']['label']}")
    print(f"  → {analysis['interpretations']['moving_averages']['explanation']}")

    print(f"\n볼린저 밴드: {analysis['interpretations']['bollinger_bands']['label']}")
    print(f"  → {analysis['interpretations']['bollinger_bands']['explanation']}")

    print("\n✅ TechnicalIndicatorCalculator test completed!")
