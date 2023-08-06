from datetime import *

#Author Name = Ashish Jaiswal
#Email id = a.j250897@gmail.com
#Version = 1.0.0

# 1. ============DATA CONVERTER=====================
class Data:
    #for KB, MB, GB, TB, PB
    def B(val, unit):
        val = int(val)
        unit = unit.upper()
        if unit == "B":
            return float(int(val) * 1)
        elif unit == "KB":
            return float(int(val) * 1024)
        elif unit == "MB":
            return float(int(val) * 1048576)
        elif unit == "GB":
            return float(int(val) * 1073741824)
        elif unit == "TB":
            return float(int(val) * 1099511630000)
        elif unit == "PB":
            return float(int(val) * 1125899910000000)
        else:
            return "Please Check your input data"

    def KB(val, unit):
        val = int(val)
        unit = unit.upper()
        if unit == "B":
            return float(int(val) * 0.0009765625)  
        elif unit == "KB":
            return float(int(val) * 1)
        elif unit == "MB":
            return float(int(val) * 1024)
        elif unit == "GB":
            return float(int(val) * 1048576)
        elif unit == "TB":
            return float(int(val) * 1073741824)
        elif unit == "PB":
            return float(int(val) * 1099511630000)
        else:
            return "Please Check your input data"

    def MB(val, unit):
        val = int(val)
        unit = unit.upper()
        if unit == "B":
            return float(int(val) * 0.000000953674316)
        elif unit == "KB":
            return float(int(val) * 0.0009765625)  
        elif unit == "MB":
            return float(int(val) * 1)
        elif unit == "GB":
            return float(int(val) * 1024)
        elif unit == "TB":
            return float(int(val) * 1048576)
        elif unit == "PB":
            return float(int(val) * 1073741824)
        else:
            return "Please Check your input data"

    def GB(val, unit):
        val = int(val)
        unit = unit.upper()
        if unit == "B":
            return float(int(val) * 0.0000000009313225746154785)
        elif unit == "KB":
            return float(int(val) * 0.000000953674316)  
        elif unit == "MB":
            return float(int(val) * 0.0009765625)
        elif unit == "GB":
            return float(int(val) * 1)
        elif unit == "TB":
            return float(int(val) * 1024)
        elif unit == "PB":
            return float(int(val) * 1048576)
        else:
            return "Please Check your input data"

    def TB(val, unit):
        val = int(val)
        unit = unit.upper()
        if unit == "B":
            return "N/D"
        elif unit == "KB":
            return float(int(val) * 0.0000000009313225746154785)
        elif unit == "MB":
            return float(int(val) * 0.000000953674316)
        elif unit == "GB":
            return float(int(val) * 0.0009765625)
        elif unit == "TB":
            return float(int(val) * 1)
        elif unit == "PB":
            return float(int(val) * 1024)
        else:
            return "Please Check your input data"

    def PB(val, unit):
        val = int(val)
        unit = unit.upper()
        if unit == "B":
            return "N/D"
        elif unit == "KB":
            return "N/D" 
        elif unit == "MB":
            return float(int(val) * 0.0000000009313225746154785)
        elif unit == "GB":
            return float(int(val) * 0.000000953674316)
        elif unit == "TB":
            return float(int(val) * 0.0009765625)
        elif unit == "PB":
            return float(int(val) * 1)
        else:
            return "Please Check your input data"
#============DATA CONVERTER END=====================
# 2. ============BMI CONVERTER==========================
def BMI(kg,cm):
    kg = float(kg)
    cm = float(cm)
    bmi_is = (kg/cm/cm)*10000
    if bmi_is > 25.0:
        bmi_status = "OverWeight"
    elif bmi_is > 18.4:
        bmi_status = "Healthy"
    else:
        bmi_status = "UnderWeight"
    return "{:.2f}".format(bmi_is),bmi_status
#============BMI CONVERTE END=======================
# 3. ============Discount Calculate==========================
def Discount(price,percent):
    price = float(price)
    percent = float(percent)
    if percent > 100:
        return "Percent must not be greater than 100."
    else:
        discount_is = (price) - ((percent/price)*100)
        return discount_is
    return "Please Check your input data"
#============Discount Calculate END=======================
# 4. ============Date Calculate==========================
def Date(start_date, end_date, date_format='%d/%m/%Y'):
    start_date = datetime.strptime(start_date, date_format)
    end_date = datetime.strptime(end_date, date_format)
    date_diff = end_date - start_date
    return date_diff
#============Date Calculate END=======================
# 5. ============Age Calculate==========================
def Age(dob,date_format='%d/%m/%Y'):
    age_is = {}
    dob = datetime.strptime(dob, date_format)
    age_is["Year"] = datetime.now().year - dob.year
    if datetime.now().month == dob.month:
        age_is["Month"] = 0
        age_is["Day"] = datetime.now().day
    else :
        age_is["Month"] = (datetime.now().month - dob.month) - 1
        age_is["Day"] =  30 - (dob.day - datetime.now().day)
    return age_is
#============Age Calculate END=======================
# 6. ============Time Calculate==========================
class Time:
    #Day - D |Week - W | Month - M | Year - Y
    def Day(val,unit):
        unit = unit.upper()
        if unit == "D":
            return val
        elif unit == "W":
            return (val * 7)
        elif unit == "M":
            return (val * 30)
        elif unit == "Y":
            return (val * 365)
        else:
            return "Please Check your input data"

    def Week(val,unit):
        unit = unit.upper()
        if unit == "D":
            return (val / 7)
        elif unit == "W":
            return val
        elif unit == "M":
            return (val * 4)
        elif unit == "Y":
            return (val * 52)
        else:
            return "Please Check your input data"

    def Month(val,unit):
        unit = unit.upper()
        if unit == "D":
            return (val / 30)
        elif unit == "W":
            return (val / 4)
        elif unit == "M":
            return val
        elif unit == "Y":
            return (val * 12)
        else:
            return "Please Check your input data"

    def Year(val,unit):
        unit = unit.upper()
        if unit == "D":
            return (val / 365)
        elif unit == "W":
            return (val / 52)
        elif unit == "M":
            return (val / 12)
        elif unit == "Y":
            return (val)
        else:
            return "Please Check your input data"
#============Time Calculate END=======================
# 7. ============Numeric System Calculate==========================
def Decimal(val):
    numeric_data = {"Binary" : bin(val),"Octal" : oct(val), "Hexadecimal" : hex(val)}
    return numeric_data
#============Numeric Calculate END=======================
# 8. ============Temperature Calculate==========================
class Temperature:
    #for C, F, K, R, Re
    def C(val, unit):
        val = int(val)
        unit = unit.upper()
        if unit == "C":
            return val
        elif unit == "F":
            return (val-32) * (5/9)
        elif unit == "K":
            return val - 273.15
        elif unit == "R":
            return (val - 491.67) * (5/9)
        elif unit == "Re" or unit == "RE":
            return (1.25*val)
        else:
            return "Please Check your input data"
        
    def F(val, unit):
        val = int(val)
        unit = unit.upper()
        if unit == "C":
            return (val * 1.8) + 32
        elif unit == "F":
            return val
        elif unit == "K":
            return (val - 273.15) * 1.8 + 32
        elif unit == "R":
            return (val - 459.67)
        elif unit == "Re" or unit == "RE":
            return (val * 2.25) + 32
        else:
            return "Please Check your input data"

    def K(val, unit):
        val = int(val)
        unit = unit.upper()
        if unit == "C":
            return (val + 273.15)
        elif unit == "F":
            return (val - 32) * (5/9) + 273.15
        elif unit == "K":
            return (val - 273.15) * 1.8 + 32
        elif unit == "R":
            return (val - 459.67)
        elif unit == "Re" or unit == "RE":
            return (val * 1.25) + 273.15
        else:
            return "Please Check your input data"

    def R(val, unit):
        val = int(val)
        unit = unit.upper()
        if unit == "C":
            return (val * 1.8) + 491.67
        elif unit == "F":
            return val + 459.67
        elif unit == "K":
            return (val * 1.8)
        elif unit == "R":
            return val
        elif unit == "Re" or unit == "RE":
            return (val * 2.25) + 491.67
        else:
            return "Please Check your input data"

    def Re(val, unit):
        val = int(val)
        unit = unit.upper()
        if unit == "C":
            return (val*0.8)
        elif unit == "F":
            return (val * 0.45) + (-14.2)
        elif unit == "K":
            return (val * 0.8) + (-218.52)
        elif unit == "R":
            return (val * 0.44) + (-218.52)
        elif unit == "Re" or unit == "RE":
            return val
        else:
            return "Please Check your input data"
#============Temperature Calculate END=======================
# 9. ============Speed Calculate==========================
class Speed:
    # miles per hour - mph | foot per second - fps | meter per second - mps | kilometer per hour - kmh | knot - kn
    def mph(val, unit):
        unit = unit.upper()
        if unit == "MPH":
            return val
        elif unit == "FPS":
            return (val / 1.467)
        elif unit == "MPS":
            return (val * 2.237)
        elif unit == "KMH":
            return (val / 1.609)
        elif unit == "KN":
            return (val * 1.151)
        else:
            return "Please Check your input data"

    def fps(val, unit):
        unit = unit.upper()
        if unit == "MPH":
            return (val * 1.467)
        elif unit == "FPS":
            return val
        elif unit == "MPS":
            return (val * 3.281)
        elif unit == "KMH":
            return (val / 1.097)
        elif unit == "KN":
            return (val * 1.688)
        else:
            return "Please Check your input data"

    def mps(val, unit):
        unit = unit.upper()
        if unit == "MPH":
            return (val / 2.237)
        elif unit == "FPS":
            return (val / 3.281)
        elif unit == "MPS":
            return val
        elif unit == "KMH":
            return (val / 3.6)
        elif unit == "KN":
            return (val / 1.944)
        else:
            return "Please Check your input data"

    def kmh(val, unit):
        unit = unit.upper()
        if unit == "MPH":
            return (val * 1.609)
        elif unit == "FPS":
            return (val * 1.097)
        elif unit == "MPS":
            return (val * 3.6)
        elif unit == "KMH":
            return val
        elif unit == "KN":
            return (val * 1.852)
        else:
            return "Please Check your input data"

    def kn(val, unit):
        unit = unit.upper()
        if unit == "MPH":
            return (val / 1.151)
        elif unit == "FPS":
            return (val / 1.688)
        elif unit == "MPS":
            return (val * 1.944)
        elif unit == "KMH":
            return (val / 1.852)
        elif unit == "KN":
            return val
        else:
            return "Please Check your input data"
#============Speed Calculate END=======================
# 10. ============Pressure Calculate==========================
class Pressure:
    # Pascal - Pa | Bar | Pound per square inch - Psi | Standard Atmosphere - atm | Torr
    def Pa(val, unit):
        unit = unit.upper()
        if unit == "PA":
            return val
        elif unit == "BAR":
            return (val * 100000)
        elif unit == "PSI":
            return (val * 6895)
        elif unit == "ATM":
            return (val * 101325)
        elif unit == "TORR":
            return (val * 133)
        else:
            return "Please Check your input data"

    def Bar(val, unit):
        unit = unit.upper()
        if unit == "PA":
            return (val / 100000)
        elif unit == "BAR":
            return val
        elif unit == "PSI":
            return (val / 14.504)
        elif unit == "ATM":
            return (val * 1.013)
        elif unit == "TORR":
            return (val / 750)
        else:
            return "Please Check your input data"
    
    def Psi(val, unit):
        unit = unit.upper()
        if unit == "PA":
            return (val / 6895)
        elif unit == "BAR":
            return (val * 14.504)
        elif unit == "PSI":
            return val
        elif unit == "ATM":
            return (val * 14.696)
        elif unit == "TORR":
            return (val / 51.715)
        else:
            return "Please Check your input data"

    def Atm(val, unit):
        unit = unit.upper()
        if unit == "PA":
            return (val / 101325)
        elif unit == "BAR":
            return (val / 1.013)
        elif unit == "PSI":
            return (val / 14.696)
        elif unit == "ATM":
            return val
        elif unit == "TORR":
            return (val / 760)
        else:
            return "Please Check your input data"

    def Torr(val, unit):
        unit = unit.upper()
        if unit == "PA":
            return (val / 133)
        elif unit == "BAR":
            return (val * 750)
        elif unit == "PSI":
            return (val * 51.715)
        elif unit == "ATM":
            return (val * 760)
        elif unit == "TORR":
            return val
        else:
            return "Please Check your input data"
#============Pressure Calculate END=======================
# 11. ============GST Calculate===========================
def GST(price,percent):
    gst_is = {}
    price = float(price)
    percent = float(percent)
    if percent > 100:
        return "Percent must not be greater than 100."
    else:
        gst_amt = ((percent/price)*100)
        gst_price = (price) + gst_amt
        gst_is = {"GST Price": gst_price, "CGST/SGST": gst_amt/2}
        return gst_is
    return "Please Check your input data"
#==============GST Calculate END=========================