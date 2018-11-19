import fractions
import math

def TrigString(a, b, k, n):
    # Construct inside of trig function
    if int(n) == 1:
        trig_coeff_str = "x"
    else:
        trig_coeff_str = "%s x" % str(n)
    
    # Construct sin expression
    if a == 0:
        sin_str = ""
    elif a == 1:
        sin_str = "sin(%s)" % trig_coeff_str
    else:
        sin_str = "sin(%s)^%d" % (trig_coeff_str, a)
    
    # Construct cos expression
    if b == 0:
        cos_str = ""
    elif b == 1:
        cos_str = "cos(%s)" % trig_coeff_str
    else:
        cos_str = "cos(%s)^%d" % (trig_coeff_str, b)

    # Construct overall expression
    if float(k) == 1.0:
        if sin_str == "" and cos_str == "":
            return "1"
        elif sin_str == "" and cos_str != "":
            return cos_str
        elif sin_str != "" and cos_str == "":
            return sin_str
        else:
            return "%s %s" % (sin_str, cos_str)
    else:
        if sin_str == "" and cos_str == "":
            return str(k)
        elif sin_str == "" and cos_str != "":
            return "%s %s" % (str(k), cos_str)
        elif sin_str != "" and cos_str == "":
            return "%s %s" % (str(k), sin_str)
        else:
            return "%s %s %s" % (str(k), sin_str, cos_str)

class Integral(object):
    def __init__(self, a=0, b=0, k=fractions.Fraction(1, 1), n=fractions.Fraction(1,1)):
        '''An indefinite integral in the format integral {k (sin(nx))^a (cos(nx))^b dx}'''
        if type(a) is not int or a < 0:
            raise TypeError("Sine exponent must be a positive integer or 0")
        self.a = a

        if type(b) is not int:
            raise TypeError("Cosine exponent must be a positive integer or 0")
        self.b = b

        if type(k) is str:
            self.k = fractions.Fraction(k)
        elif type(k) is int:
            self.k = fractions.Fraction(k, 1)
        elif type(k) is fractions.Fraction:
            self.k = k
        else:
            raise TypeError("Outside coefficient must be an integer, fraction, or fraction string")
        
        if type(n) is str:
            self.n = fractions.Fraction(n)
        elif type(n) is int:
            self.n = fractions.Fraction(n, 1)
        elif type(n) is fractions.Fraction:
            self.n = n
        else:
            raise TypeError("Inside coefficient must be an integer, fraction, or fraction string")
        if int(self.n) == 0:
            raise ValueError("Inside coefficient must be non-zero")

    def __str__(self):
        return "integral {%s dx}" % TrigString(self.a, self.b, self.k, self.n)

    def Eval(self):
        '''Ultimately returns a list of strings representing a sum of expressions'''
        if self.a == 0 and self.b == 0:
            # integral {k dx}
            #  => kx
            return "%s x" % str(self.k)

        elif self.a == 1:
            # integral {k sin(nx) (cos(nx))^b dx}
            #  => -k/n/(b+1) (cos(nx))^(b+1)
            k_coeff = -self.k / self.n * fractions.Fraction(1, self.b + 1)
            return TrigString(0, self.b + 1, k_coeff, self.n)

        elif self.b == 1:
            # integral {k (sin(nx))^a cos(nx) dx}
            #  => k/n/(a+1) (sin(nx))^(a+1)
            k_coeff = self.k / self.n * fractions.Fraction(1, self.a + 1)
            return TrigString(self.a + 1, 0, k_coeff, self.n)

        elif self.a == 0:
            # integral {k (cos(nx))^b dx}
            #  => k/n/b sin(nx) (cos(nx))^(b-1) + 
            #     integral {k (b-1)/b (cos(nx))^(b-2) dx}
            
            # Integration by parts: uv
            uv_k_coeff = self.k / self.n * fractions.Fraction(1, self.b)
            uv_string = TrigString(1, self.b - 1, uv_k_coeff, self.n)

            # Integration by parts: v du
            vdu_k_coeff = self.k * fractions.Fraction(self.b - 1, self.b)
            vdu_integral = Integral(0, self.b - 2, vdu_k_coeff, self.n)
            vdu_string = vdu_integral.Eval()

            if vdu_string[0] == "-":
                return "%s - %s" % (uv_string, vdu_string[1:])
            else:
                return "%s + %s" % (uv_string, vdu_string)

        elif self.b == 0:
            # integral {k (sin(nx))^a dx}
            #  => -k/n/a cos(nx) (sin(nx))^(a-1) + 
            #     integral {k (a-1)/a (sin(nx))^(a-2) dx}
            
            # Integration by parts: uv
            uv_k_coeff = -self.k / self.n * fractions.Fraction(1, self.a)
            uv_string = TrigString(self.a - 1, 1, uv_k_coeff, self.n)

            # Integration by parts: v du
            vdu_k_coeff = self.k * fractions.Fraction(self.a - 1, self.a)
            vdu_integral = Integral(self.a - 2, 0, vdu_k_coeff, self.n)
            vdu_string = vdu_integral.Eval()

            if vdu_string[0] == "-":
                return "%s - %s" % (uv_string, vdu_string[1:])
            else:
                return "%s + %s" % (uv_string, vdu_string)

        elif (self.a % 2 == 0 and self.b % 2 == 0) or (self.a % 2 == 1 and self.b % 2 == 1):
            # integral {k (sin(nx))^a (cos(nx))^b dx}, a and b are both even or both odd
            #  => integral {k (1/2 sin(2nx))^a (1/2 + 1/2 cos(2nx))^((b - a)/2) dx}, b > a
            #  => integral {k (1/2 sin(2nx))^b (1/2 - 1/2 cos(2nx))^((a - b)/2) dx}, a > b
            #  => integral {k (1/2 sin(2nx))^a dx}, a = b

            # Get the sine term
            sin_exp = min(self.a, self.b)
            sin_k = fractions.Fraction(1, 2) ** sin_exp

            # No cosine terms if a = b
            if self.a == self.b:
                integral = Integral(self.a, 0, self.k * sin_k, self.n * 2)
                return integral.Eval()
            
            # Get the cosine terms
            if (sin_exp == self.a):
                # There are extra cosines, b > a
                cos_exp = int((self.b - self.a) / 2)
                binomial_b = fractions.Fraction(1, 2)
            else:
                # There are extra sines, a > b
                cos_exp = int((self.a - self.b) / 2)
                binomial_b = fractions.Fraction(-1, 2)
            # Binomial expansion coefficients
            bin_k = [fractions.Fraction(math.factorial(cos_exp), math.factorial(r) * math.factorial(cos_exp - r)) for r in range(0, cos_exp + 1)]
            cos_k = [bin_k[n] * fractions.Fraction(1, 2)**(cos_exp - n) * binomial_b**n for n in range(0, cos_exp + 1)]

            # Create a list of sub-integrals to evaluate
            integrals = [Integral(sin_exp, b, self.k * sin_k * cos_k[b], self.n * 2) for b in range(0, cos_exp + 1)]
            integral_strings = [integral.Eval() for integral in integrals]
            output = integral_strings[0]
            for string in integral_strings[1:]:
                if string[0] == "-":
                    output += " - " + string[1:]
                else:
                    output += " + " + string
            return output

        elif self.a % 2 == 0 and self.b % 2 == 1:
            # integral {k (sin(nx))^a (cos(nx))^b dx}, a is even and b is odd
            #  => integral {k (cos(nx))^b (1 - (cos(nx))^2)^(a/2) dx}
            cos_exp = int(self.a / 2)
            bin_k = [fractions.Fraction(math.factorial(cos_exp), math.factorial(r) * math.factorial(cos_exp - r)) for r in range(0, cos_exp + 1)]
            cos_k = [bin_k[n] * (-1)**n for n in range(0, cos_exp + 1)]

            # Create a list of sub-integrals to evaluate
            integrals = [Integral(0, self.b + b * 2, self.k * cos_k[b], self.n) for b in range(0, cos_exp + 1)]
            integral_strings = [integral.Eval() for integral in integrals]
            output = integral_strings[0]
            for string in integral_strings[1:]:
                if string[0] == "-":
                    output += " - " + string[1:]
                else:
                    output += " + " + string
            return output

        elif self.a % 2 == 1 and self.b % 2 == 0:
            # integral {k (sin(nx))^a (cos(nx))^b dx}, a is odd and b is even
            #  => integral {k (sin(nx))^a (1 - (sin(nx))^2)^(b/2) dx}
            sin_exp = int(self.b / 2)
            bin_k = [fractions.Fraction(math.factorial(sin_exp), math.factorial(r) * math.factorial(sin_exp - r)) for r in range(0, sin_exp + 1)]
            sin_k = [bin_k[n] * (-1)**n for n in range(0, sin_exp + 1)]
            print(str(self))
            print(sin_k)

            # Create a list of sub-integrals to evaluate
            integrals = [Integral(self.a + a * 2, 0, self.k * sin_k[a], self.n) for a in range(0, sin_exp + 1)]
            for i in integrals: print(i)
            integral_strings = [integral.Eval() for integral in integrals]
            output = integral_strings[0]
            for string in integral_strings[1:]:
                if string[0] == "-":
                    output += " - " + string[1:]
                else:
                    output += " + " + string
            return output

        else:
            return str(self)

const = Integral(3, 7, 1, 5)
print(const.Eval())
