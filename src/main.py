"""小型且可测试的金融计算示例。"""

from decimal import Decimal, ROUND_HALF_UP


MONEY = Decimal("0.01")


def calculate_simple_interest(
    principal: Decimal,
    annual_rate: Decimal,
    years: Decimal,
) -> Decimal:
    """计算单利，并将结果四舍五入到两位小数。

    ``annual_rate`` 使用小数表示，例如 5% 应写成 ``Decimal("0.05")``。
    使用 Decimal 而不是 float，可以避免金额计算中的二进制浮点误差。
    """
    if principal < 0:
        raise ValueError("principal must not be negative")
    if annual_rate < 0:
        raise ValueError("annual_rate must not be negative")
    if years < 0:
        raise ValueError("years must not be negative")

    interest = principal * annual_rate * years
    return interest.quantize(MONEY, rounding=ROUND_HALF_UP)


def main() -> None:
    """运行一个不包含真实金融数据的小型演示。"""
    principal = Decimal("10000")
    annual_rate = Decimal("0.035")
    years = Decimal("1")
    interest = calculate_simple_interest(principal, annual_rate, years)
    print(f"Simple interest: {interest}")


if __name__ == "__main__":
    main()
