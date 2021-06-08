from numpy import interp, polyfit, poly1d


class CalculatingModule:
    def __init__(self, max_power):
        self.max_power = max_power
        self.RF_volt = [0.2, 0.32, 0.4, 0.44, 0.5, 0.52, 0.56, 0.6, 0.64,
                        0.68, 0.7, 0.72, 0.76, 0.8, 0.84, 0.88, 0.9, 0.92, 0.96, 1]
        self.RF_power = [0.075, 0.47, 2.1, 3.8, 5.3, 7.7, 10.8, 13.5,
                         17.8, 21.5, 23, 25.7, 28.3, 31, 34, 36, 36.5, 38, 39.2, 40]
# last data (with lens)
        # self.coef_volt = [0.52, 0.7, 1.64, 2, 2.52, 3.16, 3.5, 4,
        #                   4.4, 4.8, 5, 5.5, 6.26, 6.7, 7.12, 7.76]
        # self.coef_power = [0.04, 0.05, 0.143, 0.2, 0.26, 0.32, 0.38, 0.42,
        #                    0.43, 0.51, 0.49, 0.6, 0.636, 0.735, 0.74, 0.825]
# old data (without lens)
        self.coef_power = [0.02, 0.1, 0.25, 0.45, 0.66, 0.823, 0.95, 1.03, 1.35,
                           1.45, 1.6, 1.68, 1.7, 1.97, 2.25, 2.52, 2.9, 2.94, 3.1, 3.48, 3.7, 4, 4.3]

        self.coef_volt = [0.2, 0.3, 0.4, 0.6, 0.8, 1, 1.08, 1.15, 1.48, 1.56, 1.67,
                          1.752, 1.78, 2.02, 2.3, 2.54, 2.74, 2.8, 3.04, 3.34, 3.6, 3.88, 4.2]

        for i in range(len(self.coef_volt)):
            self.coef_volt[i] = self.coef_volt[i] - 0.2

        coefficients = polyfit(self.coef_volt, self.coef_power, 1)
        self.p = poly1d(coefficients)

    def change_max_power(self, max_power):
        self.max_power = max_power

    def RF_from_pwr_to_volt(self, power):
        k = self.max_power / self.RF_power[(len(self.RF_power) - 1)]
        RF_power_scaled = [k*i for i in self.RF_power]
        necessary_volt = interp(power, RF_power_scaled, self.RF_volt)
        returned_val = float(necessary_volt)
        return returned_val

    def from_power_to_volt(self, power_val):
        volt_val = interp(power_val, self.coef_power, self.coef_volt)
        return float(volt_val)

    def from_volt_to_power(self, volt_val):
        # power_val = interp(volt_val, self.coef_volt, self.coef_power)
        # without negative velues
        power_val = self.p(volt_val)
        # with negative :((
        return (power_val)
