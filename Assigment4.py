import math
from abc import ABC, abstractmethod


class PetroleumFormula(ABC):
    """Abstract base class for all petroleum engineering formulas"""

    def _init_(self, name, description):
        self.name = name
        self.description = description

    @abstractmethod
    def calculate(self, **kwargs):
        pass

    def _str_(self):
        return f"{self.name}: {self.description}"


class MaterialBalance(PetroleumFormula):
    """Material Balance Equation for reservoir engineering"""

    def _init_(self):
        super()._init_("Material Balance Equation",
                       "N = (Np * Bo + (Gp - Np * Rs) * Bg + Wp * Bw) / ((Bo - Boi) + (Rsi - Rs) * Bg + m * Boi * (Bg/Bgi - 1))")

    def calculate(self, Np=None, Bo=None, Gp=None, Rs=None, Bg=None, Wp=None,
                  Bw=None, Boi=None, Rsi=None, m=None, Bgi=None, N=None):
        try:
            # Calculate original oil in place (N) if not provided
            if N is None:
                numerator = Np * Bo + (Gp - Np * Rs) * Bg + Wp * Bw
                denominator = (Bo - Boi) + (Rsi - Rs) * Bg + m * Boi * (Bg / Bgi - 1)

                if denominator == 0:
                    raise ValueError("Denominator cannot be zero")

                return numerator / denominator
            # Or calculate cumulative oil production (Np) if N is provided
            else:
                # This is a simplified approach for demonstration
                term = (Bo - Boi) + (Rsi - Rs) * Bg + m * Boi * (Bg / Bgi - 1)
                return (N * term - (Gp - Np * Rs) * Bg - Wp * Bw) / Bo

        except (TypeError, ValueError, ZeroDivisionError) as e:
            print(f"Error in Material Balance calculation: {e}")
            return None


class DarcyFlow(PetroleumFormula):
    """Darcy's Law for fluid flow in porous media"""

    def _init_(self):
        super()._init_("Darcy's Law", "Q = (k * A * ΔP) / (μ * L)")

    def calculate(self, k=None, A=None, deltaP=None, mu=None, L=None, Q=None):
        try:
            # Calculate flow rate if not provided
            if Q is None:
                if any(x is None or x <= 0 for x in [k, A, deltaP, mu, L]):
                    raise ValueError("All parameters must be positive values")
                return (k * A * deltaP) / (mu * L)
            # Or calculate permeability if Q is provided
            elif k is None:
                if any(x is None or x <= 0 for x in [Q, A, deltaP, mu, L]):
                    raise ValueError("All parameters must be positive values")
                return (Q * mu * L) / (A * deltaP)
            # Other variations could be implemented similarly
            else:
                raise ValueError("Insufficient parameters provided")

        except (TypeError, ValueError, ZeroDivisionError) as e:
            print(f"Error in Darcy Flow calculation: {e}")
            return None


class ProductivityIndex(PetroleumFormula):
    """Productivity Index formula"""

    def _init_(self):
        super()._init_("Productivity Index", "J = Q / (Pr - Pwf)")

    def calculate(self, Q=None, Pr=None, Pwf=None, J=None):
        try:
            if J is None:
                if any(x is None for x in [Q, Pr, Pwf]):
                    raise ValueError("Q, Pr, and Pwf must be provided")
                if Pr <= Pwf:
                    raise ValueError("Reservoir pressure must be greater than flowing bottomhole pressure")
                return Q / (Pr - Pwf)
            elif Q is None:
                if any(x is None for x in [J, Pr, Pwf]):
                    raise ValueError("J, Pr, and Pwf must be provided")
                if Pr <= Pwf:
                    raise ValueError("Reservoir pressure must be greater than flowing bottomhole pressure")
                return J * (Pr - Pwf)
            else:
                raise ValueError("Insufficient parameters provided")

        except (TypeError, ValueError, ZeroDivisionError) as e:
            print(f"Error in Productivity Index calculation: {e}")
            return None


class VogelEquation(PetroleumFormula):
    """Vogel's Equation for IPR curve"""

    def _init_(self):
        super()._init_("Vogel's Equation", "Q / Qmax = 1 - 0.2 * (Pwf/Pr) - 0.8 * (Pwf/Pr)^2")

    def calculate(self, Q=None, Qmax=None, Pwf=None, Pr=None):
        try:
            if Qmax is None:
                if any(x is None or x <= 0 for x in [Q, Pwf, Pr]):
                   raise ValueError("All parameters must be positive values")
                if Pwf > Pr:
                  raise ValueError("Flowing pressure cannot exceed reservoir pressure")
                return Q / (1 - 0.2 * (Pwf / Pr) - 0.8 * (Pwf / Pr) ** 2)

            elif Q is None:
                return Qmax * (1 - 0.2 * (Pwf / Pr) - 0.8 * (Pwf / Pr) ** 2)

            else:
                raise ValueError("Insufficient parameters provided")
        except ValueError as e:
            return f"Error: {e}"


class DeclineCurve(PetroleumFormula):
    """Arps Decline Curve Analysis"""

    def _init_(self):
        super()._init_("Arps Decline Curve: Q = Qi / (1 + b * Di * t)^(1/b)")

    def calculate(self, Qi=None, b=None, Di=None, t=None, Q=None):
        try:
            if Q is None:
                if any(x is None or x < 0 for x in [Qi, b, Di, t]):
                    raise ValueError("All parameters must be non-negative")
                if b == 0:  # Exponential decline
                    return Qi * math.exp(-Di * t)
                else:  # Hyperbolic decline
                    return Qi / (1 + b * Di * t) ** (1 / b)
            elif Qi is None:
                if b == 0:
                    return Q / math.exp(-Di * t)
                else:
                    return Q * (1 + b * Di * t) ** (1 / b)
            else:
                raise ValueError("Insufficient parameters provided")
        except ValueError as e:
            return f"Error: {e}"

class PVTCorrelation(PetroleumFormula):
            """Standing's PVT Correlation for bubble point pressure"""

            def _init_(self):
                super()._init_(
                    "Standing's Correlation: Pb = 18.2 * ((Rs/γg)^0.83 * 10^(0.00091*T - 0.0125*°API) - 1.4)")

            def calculate(self, Rs=None, gamma_g=None, T=None, API=None, Pb=None):
                try:
                    if Pb is None:
                        if any(x is None or x <= 0 for x in [Rs, gamma_g, T, API]):
                            raise ValueError("All parameters must be positive")
                        return 18.2 * ((Rs / gamma_g) ** 0.83 * 10 ** (0.00091 * T - 0.0125 * API) - 1.4)
                    elif Rs is None:
                        inner_term = (Pb / 18.2 + 1.4) / (10 ** (0.00091 * T - 0.0125 * API))
                        return gamma_g * (inner_term ** (1 / 0.83))
                    else:
                        raise ValueError("Insufficient parameters provided")
                except ValueError as e:
                    return f"Error: {e}"

class MaterialBalance(PetroleumFormula):
                    """Simplified Material Balance Equation"""

                    def _init_(self):
                        super()._init_("Material Balance: N = Np * Bo / (Bo - Boi)")

                    def calculate(self, Np=None, Bo=None, Boi=None, N=None):
                        try:
                            if N is None:
                                if any(x is None or x <= 0 for x in [Np, Bo, Boi]):
                                    raise ValueError("All parameters must be positive")
                                if Bo <= Boi:
                                    raise ValueError("Current FVF must be greater than initial")
                                return Np * Bo / (Bo - Boi)
                            elif Np is None:
                                return N * (Bo - Boi) / Bo
                            else:
                                raise ValueError("Insufficient parameters provided")
                        except ValueError as e:
                            return f"Error: {e}"

                # Demonstration
                    #
if __name__ == "__main__":
                    # Create formula objects
                    formulas = [
                        DarcyFlow(),
                        ProductivityIndex(),
                        VogelEquation(),
                        DeclineCurve(),
                        PVTCorrelation(),
                        MaterialBalance()
                    ]
        # Demonstrate calculations
                    print("Petroleum Engineering Formulas Calculator\n")

                    # Darcy's Law example
                    darcy = formulas[0]
                    print(darcy)
                    result = darcy.calculate(k=0.1, A=100, deltaP=500, mu=2, L=50)
                    print(f"Flow rate: {result:.2f} bbl/day\n")

                    # Productivity Index example
                    pi = formulas[1]
                    print(pi)
                    result = pi.calculate(Q=1000, Pr=3000, Pwf=2000)
                    print(f"Productivity Index: {result:.2f} bbl/day/psi\n")

                    # Vogel's Equation example
                    vogel = formulas[2]
                    print(vogel)
                    result = vogel.calculate(Qmax=2000, Pwf=1500, Pr=3000)
                    print(f"Flow rate: {result:.2f} bbl/day\n")

                    # Decline Curve example
                    decline = formulas[3]
                    print(decline)
                    result = decline.calculate(Qi=1000, b=0.5, Di=0.1, t=365)
                    print(f"Production after 1 year: {result:.2f} bbl/day\n")

                    # PVT Correlation example
                    pvt = formulas[4]
                    print(pvt)
                    result = pvt.calculate(Rs=500, gamma_g=0.65, T=180, API=35)
                    print(f"Bubble point pressure: {result:.2f} psi\n")

                    # Material Balance example
                    mb = formulas[5]
                    print(mb)
                    result = mb.calculate(Np=1e6, Bo=1.2, Boi=1.1)
                    print(f"Original oil in place: {result:.2e} STB\n")
                   # Demonstrate calculations
                    print("Petroleum Engineering Formulas Calculator\n")

                    # Darcy's Law example
                    darcy = formulas[0]
                    print(darcy)
                    result = darcy.calculate(k=0.1, A=100, deltaP=500, mu=2, L=50)
                    print(f"Flow rate: {result:.2f} bbl/day\n")

                    # Productivity Index example
                    pi = formulas[1]
                    print(pi)
                    result = pi.calculate(Q=1000, Pr=3000, Pwf=2000)
                    print(f"Productivity Index: {result:.2f} bbl/day/psi\n")

                    # Vogel's Equation example
                    vogel = formulas[2]
                    print(vogel)
                    result = vogel.calculate(Qmax=2000, Pwf=1500, Pr=3000)
                    print(f"Flow rate: {result:.2f} bbl/day\n")

                    # Decline Curve example
                    decline = formulas[3]
                    print(decline)
                    result = decline.calculate(Qi=1000, b=0.5, Di=0.1, t=365)
                    print(f"Production after 1 year: {result:.2f} bbl/day\n")

                    # PVT Correlation example
                    pvt = formulas[4]
                    print(pvt)
                    result = pvt.calculate(Rs=500, gamma_g=0.65, T=180, API=35)
                    print(f"Bubble point pressure: {result:.2f} psi\n")

                    # Material Balance example
                    mb = formulas[5]
                    print(mb)
                    result = mb.calculate(Np=1e6, Bo=1.2, Boi=1.1)
                    print(f"Original oil in place: {result:.2e} STB\n")