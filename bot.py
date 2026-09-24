import json
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer,
    Table, TableStyle
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER

# ============================================
# COMPLETE DATA
# ============================================
data = [
    {
        "id": 1,
        "section": "A - Profit & Loss",
        "question": "A wrist watch purchased for Rs.3,000 sold for Rs.3,500. Find profit %.",
        "options": {"a": "20.50%", "b": "18.33%", "c": "16.66%", "d": "19.58%"},
        "correct_answer": "c",
        "correct_value": "16.66%",
        "solution": {
            "steps": ["Profit = 3500-3000 = Rs.500", "Profit% = (500/3000)x100 = 16.66%"],
            "trick": "Profit% = (Profit/CP) x 100"
        }
    },
    {
        "id": 2,
        "section": "A - Profit & Loss",
        "question": "Shopkeeper buys groundnuts Rs.64/kg sells Rs.80/kg but gives 800g instead of 1kg. Actual profit %?",
        "options": {"a": "28.75%", "b": "36.65%", "c": "56.25%", "d": "32.25%"},
        "correct_answer": "c",
        "correct_value": "56.25%",
        "solution": {
            "steps": ["CP of 800g = (64/1000)x800 = Rs.51.20", "Profit% = (80-51.20)/51.20 x100 = 56.25%"],
            "trick": "Actual CP = cost of quantity actually given"
        }
    },
    {
        "id": 3,
        "section": "A - Profit & Loss",
        "question": "Laptop Rs.56,000 (20% profit) + scanner Rs.22,000 (15% profit). Overall profit %?",
        "options": {"a": "18 23/39%", "b": "18 21/37%", "c": "12 21/37%", "d": "12 23/39%"},
        "correct_answer": "a",
        "correct_value": "18 23/39%",
        "solution": {
            "steps": ["Total CP = 56000+22000 = Rs.78,000", "Total SP = 67200+25300 = Rs.92,500", "Profit% = 14500/78000 x100 = 18 23/39%"],
            "trick": "Calculate SP of each separately then find overall profit%"
        }
    },
    {
        "id": 4,
        "section": "A - Profit & Loss",
        "question": "Selling hair oil at Rs.336 gives 12% gain. For 9% gain, new SP?",
        "options": {"a": "Rs.339", "b": "Rs.330", "c": "Rs.300", "d": "Rs.327"},
        "correct_answer": "d",
        "correct_value": "Rs.327",
        "solution": {
            "steps": ["CP = 336/1.12 = Rs.300", "New SP = 300 x 1.09 = Rs.327"],
            "trick": "First find CP, then calculate new SP"
        }
    },
    {
        "id": 5,
        "section": "A - Profit & Loss",
        "question": "Dealer sells at Rs.850 after 15% discount. Without discount 25% profit. Find CP.",
        "options": {"a": "Rs.950", "b": "Rs.1000", "c": "Rs.900", "d": "Rs.800"},
        "correct_answer": "d",
        "correct_value": "Rs.800",
        "solution": {
            "steps": ["MP = 850/0.85 = Rs.1000", "CP = 1000/1.25 = Rs.800"],
            "trick": "SP to MP to CP chain: use discount% then profit%"
        }
    },
    {
        "id": 6,
        "section": "A - Profit & Loss",
        "question": "Profit at SP Rs.1200 = Loss at SP Rs.900. SP for 20% gain?",
        "options": {"a": "Rs.1260", "b": "Rs.1300", "c": "Rs.1150", "d": "Rs.1250"},
        "correct_answer": "a",
        "correct_value": "Rs.1260",
        "solution": {
            "steps": ["CP = (1200+900)/2 = Rs.1050", "New SP = 1050 x 1.20 = Rs.1260"],
            "trick": "When profit=loss, CP = average of two SPs"
        }
    },
    {
        "id": 7,
        "section": "A - Profit & Loss",
        "question": "30kg tea @Rs.400 mixed with 20kg @Rs.500, sold @Rs.480/kg. Profit %?",
        "options": {"a": "8.5%", "b": "9.09%", "c": "10%", "d": "11.11%"},
        "correct_answer": "b",
        "correct_value": "9.09%",
        "solution": {
            "steps": ["Total CP = 12000+10000 = Rs.22,000", "Total SP = 50x480 = Rs.24,000", "Profit% = 2000/22000 x100 = 9.09%"],
            "trick": "Calculate total CP and total SP separately"
        }
    },
    {
        "id": 8,
        "section": "A - Profit & Loss",
        "question": "Max discount: (1) 25%+15% successive (2) 20% single (3) 2 free on 3 (4) 3 free on 7?",
        "options": {"a": "Scheme 1", "b": "Scheme 2", "c": "Scheme 3", "d": "Scheme 4"},
        "correct_answer": "c",
        "correct_value": "Scheme 3",
        "solution": {
            "steps": ["Scheme1=36.25%, Scheme2=20%, Scheme3=40%, Scheme4=30%", "Maximum discount = Scheme 3 (40%)"],
            "trick": "Free items discount = free/(total) x100"
        }
    },
    {
        "id": 9,
        "section": "B - Average",
        "question": "Avg of 12 numbers=47. First 5 avg=45, next 4 avg=52. 10th=11th-10=12th+5. Avg of 11th & 12th?",
        "options": {"a": "46.5", "b": "47.5", "c": "44.5", "d": "42.5"},
        "correct_answer": "c",
        "correct_value": "44.5",
        "solution": {
            "steps": ["Sum(10,11,12)=564-225-208=131", "Let 11th=x: (x-10)+x+(x-15)=131, x=52", "Avg=(52+37)/2=44.5"],
            "trick": "Find remaining sum, then use given relations"
        }
    },
    {
        "id": 10,
        "section": "B - Average",
        "question": "Cricketer avg 45 in 14 innings. Runs in 15th inning to raise avg to 47?",
        "options": {"a": "70", "b": "75", "c": "68", "d": "72"},
        "correct_answer": "b",
        "correct_value": "75",
        "solution": {
            "steps": ["Required total = 15x47 = 705", "Current total = 14x45 = 630", "15th inning = 705-630 = 75"],
            "trick": "New score = New total - Old total"
        }
    },
    {
        "id": 11,
        "section": "B - Average",
        "question": "15 students avg 70kg. 5 more (65,68,45,77,62kg) join. Change in avg?",
        "options": {"a": "Decreases 2kg", "b": "Increases 1kg", "c": "Decreases 1kg", "d": "Increases 2kg"},
        "correct_answer": "a",
        "correct_value": "Decreases by 2 kg",
        "solution": {
            "steps": ["New sum = 1050+317 = 1367", "New avg = 1367/20 = 68.35", "Decrease approx 2kg"],
            "trick": "New avg = New total sum / New total count"
        }
    },
    {
        "id": 12,
        "section": "B - Average",
        "question": "6 numbers avg=4. Two avg=3.5, other two avg=3.75. Remaining two avg?",
        "options": {"a": "8.375", "b": "4.85", "c": "4.65", "d": "4.75"},
        "correct_answer": "d",
        "correct_value": "4.75",
        "solution": {
            "steps": ["Total = 6x4 = 24", "First four sum = 7+7.5 = 14.5", "Remaining = 9.5, Avg = 4.75"],
            "trick": "Always work with SUMS not averages"
        }
    },
    {
        "id": 13,
        "section": "B - Average",
        "question": "Group of 10, avg age increases 1.5 yrs when person aged 25 replaced. New person age?",
        "options": {"a": "35", "b": "45", "c": "40", "d": "50"},
        "correct_answer": "c",
        "correct_value": "40",
        "solution": {
            "steps": ["Total increase = 10x1.5 = 15", "New age = 25+15 = 40"],
            "trick": "New person age = Old age + (n x avg change)"
        }
    },
    {
        "id": 14,
        "section": "C - Work & Time",
        "question": "8 labourers x 10hr/day complete work in 18 days. 5 labourers finish in 24 days. hr/day?",
        "options": {"a": "10 hrs", "b": "12 hrs", "c": "8 hrs", "d": "9 hrs"},
        "correct_answer": "b",
        "correct_value": "12 hours",
        "solution": {
            "steps": ["Total work = 8x10x18 = 1440 man-hrs", "hrs/day = 1440/(5x24) = 12"],
            "trick": "M1xH1xD1 = M2xH2xD2"
        }
    },
    {
        "id": 15,
        "section": "C - Work & Time",
        "question": "A (15 days) & B (30 days) work together. A leaves after 3 days. B's remaining days?",
        "options": {"a": "21 days", "b": "24 days", "c": "32 days", "d": "28 days"},
        "correct_answer": "a",
        "correct_value": "21 days",
        "solution": {
            "steps": ["Work in 3 days = 3x(1/10) = 3/10", "Remaining = 7/10", "B alone = (7/10)x30 = 21 days"],
            "trick": "Find remaining work, then divide by B's rate"
        }
    },
    {
        "id": 16,
        "section": "C - Work & Time",
        "question": "A (9d), B (12d), C (18d). A works 3d, B works 3d, C finishes. C's days?",
        "options": {"a": "7", "b": "7.5", "c": "8", "d": "8.5"},
        "correct_answer": "b",
        "correct_value": "7.5",
        "solution": {
            "steps": ["A does 1/3, B does 1/4", "Remaining = 1-7/12 = 5/12", "C days = (5/12)x18 = 7.5"],
            "trick": "LCM method: Total=36 units, A=4/day, B=3/day, C=2/day"
        }
    },
    {
        "id": 17,
        "section": "C - Work & Time",
        "question": "A (12d), B (15d) contract Rs.9600. With C they finish in 5d. C gets?",
        "options": {"a": "Rs.2000", "b": "Rs.2400", "c": "Rs.2800", "d": "Rs.3000"},
        "correct_answer": "b",
        "correct_value": "Rs.2,400",
        "solution": {
            "steps": ["C rate = 1/5-1/12-1/15 = 1/20", "C work in 5 days = 1/4", "C share = (1/4)x9600 = Rs.2400"],
            "trick": "Share proportional to work done"
        }
    },
    {
        "id": 18,
        "section": "C - Work & Time",
        "question": "A (20d) works alone. Every 3rd day B (30d) assists. Total days to finish?",
        "options": {"a": "15d", "b": "16d", "c": "16.67d", "d": "18d"},
        "correct_answer": "c",
        "correct_value": "16.67 days",
        "solution": {
            "steps": ["3-day cycle work = 3/20+1/30 = 11/60", "5 cycles(15d) = 55/60", "Remaining = 5/60, A finishes in 5/3 days"],
            "trick": "Find work per cycle, multiply cycles, handle remainder"
        }
    },
    {
        "id": 19,
        "section": "D - Simple & Compound Interest",
        "question": "Rs.1,250 at 5.5% SI per annum for 3 years. Find interest.",
        "options": {"a": "Rs.206.25", "b": "Rs.200.00", "c": "Rs.215.75", "d": "Rs.210.25"},
        "correct_answer": "a",
        "correct_value": "Rs.206.25",
        "solution": {
            "steps": ["SI = PxRxT/100", "SI = 1250x5.5x3/100 = Rs.206.25"],
            "trick": "Direct formula: SI = PRT/100"
        }
    },
    {
        "id": 20,
        "section": "D - Simple & Compound Interest",
        "question": "Rs.5,575 at 8% SI for 4 years. Interest payable?",
        "options": {"a": "Rs.1776", "b": "Rs.1782", "c": "Rs.1788", "d": "Rs.1784"},
        "correct_answer": "d",
        "correct_value": "Rs.1784",
        "solution": {
            "steps": ["SI = 5575x8x4/100", "SI = 178400/100 = Rs.1784"],
            "trick": "Be careful with calculation, options are very close"
        }
    },
    {
        "id": 21,
        "section": "D - Simple & Compound Interest",
        "question": "CI-SI on a sum for 2 years at 15% p.a. = Rs.225. Find sum.",
        "options": {"a": "Rs.8000", "b": "Rs.9000", "c": "Rs.10000", "d": "Rs.12000"},
        "correct_answer": "c",
        "correct_value": "Rs.10,000",
        "solution": {
            "steps": ["CI-SI (2yr) = P x (R/100)^2", "225 = P x (0.15)^2 = P x 0.0225", "P = Rs.10,000"],
            "trick": "Shortcut: CI-SI for 2 years = P(r/100)^2"
        }
    },
    {
        "id": 22,
        "section": "D - Simple & Compound Interest",
        "question": "Sum doubles in 6 years under CI. Years to become 8 times?",
        "options": {"a": "12 years", "b": "24 years", "c": "18 years", "d": "16 years"},
        "correct_answer": "c",
        "correct_value": "18 years",
        "solution": {
            "steps": ["Doubles in 6 years = 2^1 in 6 yrs", "8 = 2^3, needs 3 doublings", "Time = 3x6 = 18 years"],
            "trick": "If doubles in T years, 2^n times in nxT years"
        }
    },
    {
        "id": 23,
        "section": "E - Ratio & Partnership",
        "question": "A:B=8:13, B:C=5:8, C:D=4:5. Find A:B:C:D.",
        "options": {"a": "20:50:105:119", "b": "40:65:104:130", "c": "40:60:103:112", "d": "38:65:111:120"},
        "correct_answer": "b",
        "correct_value": "40:65:104:130",
        "solution": {
            "steps": ["A:B=40:65 (LCM of 13,5=65)", "B:C=65:104", "D=104x5/4=130"],
            "trick": "Make common element equal using LCM"
        }
    },
    {
        "id": 24,
        "section": "E - Ratio & Partnership",
        "question": "A (Rs.50k) & B (Rs.70k) invest 1 year. Total profit Rs.24,000. A's share?",
        "options": {"a": "Rs.10,000", "b": "Rs.14,000", "c": "Rs.12,000", "d": "Rs.9,000"},
        "correct_answer": "a",
        "correct_value": "Rs.10,000",
        "solution": {
            "steps": ["Ratio = 50:70 = 5:7", "A share = (5/12)x24000 = Rs.10,000"],
            "trick": "Same time: profit ratio = investment ratio"
        }
    },
    {
        "id": 25,
        "section": "E - Ratio & Partnership",
        "question": "Cyrus:Rohan=3:2, Rohan:Mishti=7:12. Mishti got Rs.1,800 more than Cyrus. Rohan share?",
        "options": {"a": "Rs.7560", "b": "Rs.9240", "c": "Rs.8400", "d": "Rs.6300"},
        "correct_answer": "c",
        "correct_value": "Rs.8,400",
        "solution": {
            "steps": ["C:R:M = 21:14:24", "M-C = 3 parts = Rs.1800, 1 part = Rs.600", "Rohan = 14x600 = Rs.8400"],
            "trick": "Difference trick: find per unit value from given difference"
        }
    },
    {
        "id": 26,
        "section": "E - Ratio & Partnership",
        "question": "A (Rs.60k) & B (Rs.90k) invest. Total profit inc. 20% interest = Rs.40,000. B's share?",
        "options": {"a": "Rs.24,000", "b": "Rs.25,000", "c": "Rs.22,000", "d": "Rs.26,000"},
        "correct_answer": "a",
        "correct_value": "Rs.24,000",
        "solution": {
            "steps": ["Interest: A=12k, B=18k, Total=30k", "Remaining profit = 40k-30k = 10k split 2:3", "B total = 18000+6000 = Rs.24,000"],
            "trick": "Interest fixed first, remaining profit in ratio"
        }
    },
    {
        "id": 27,
        "section": "F - Speed Distance & Time",
        "question": "Truck: 75 km in 1st hour, 33 km in 2nd hour. Average speed?",
        "options": {"a": "60 km/h", "b": "54 km/h", "c": "108 km/h", "d": "42 km/h"},
        "correct_answer": "b",
        "correct_value": "54 km/h",
        "solution": {
            "steps": ["Total distance = 75+33 = 108 km", "Total time = 2 hours", "Avg speed = 108/2 = 54 km/h"],
            "trick": "Avg Speed = Total Distance / Total Time"
        }
    },
    {
        "id": 28,
        "section": "F - Speed Distance & Time",
        "question": "Two cars 100km apart meet in 1hr (opposite) and 5hrs (same direction). Faster car speed?",
        "options": {"a": "60 km/h", "b": "40 km/h", "c": "70 km/h", "d": "80 km/h"},
        "correct_answer": "a",
        "correct_value": "60 km/h",
        "solution": {
            "steps": ["u+v = 100, u-v = 20", "Adding: 2u = 120, u = 60 km/h"],
            "trick": "Opposite: u+v=dist/time | Same: u-v=dist/time"
        }
    },
    {
        "id": 29,
        "section": "F - Speed Distance & Time",
        "question": "Boat: downstream 2hrs, upstream 2.5hrs, stream speed 3km/h. Boat speed in still water?",
        "options": {"a": "20 km/h", "b": "29 km/h", "c": "25 km/h", "d": "27 km/h"},
        "correct_answer": "d",
        "correct_value": "27 km/h",
        "solution": {
            "steps": ["2(b+3) = 2.5(b-3)", "2b+6 = 2.5b-7.5", "b = 27 km/h"],
            "trick": "Same distance: downstream time x speed = upstream time x speed"
        }
    },
    {
        "id": 30,
        "section": "F - Speed Distance & Time",
        "question": "Two equal-length trains cross a pole in 12s & 18s. Ratio of speeds?",
        "options": {"a": "2:3", "b": "3:2", "c": "4:3", "d": "3:4"},
        "correct_answer": "b",
        "correct_value": "3:2",
        "solution": {
            "steps": ["Same distance, speed inversely proportional to time", "Speed ratio = 18:12 = 3:2"],
            "trick": "Speed1:Speed2 = Time2:Time1 (same distance)"
        }
    },
    {
        "id": 31,
        "section": "G - Mensuration",
        "question": "Max radius circle inscribed in rectangle 18cm x 12cm. Area (cm2)?",
        "options": {"a": "28pi", "b": "36pi", "c": "136pi", "d": "72pi"},
        "correct_answer": "b",
        "correct_value": "36pi",
        "solution": {
            "steps": ["Max radius = shorter side/2 = 12/2 = 6cm", "Area = pi x 6^2 = 36pi cm2"],
            "trick": "Circle fits in shorter dimension: r = min(l,w)/2"
        }
    },
    {
        "id": 32,
        "section": "G - Mensuration",
        "question": "Rhombus: side 13cm, one diagonal 24cm. Area (cm2)?",
        "options": {"a": "60", "b": "130", "c": "110", "d": "120"},
        "correct_answer": "d",
        "correct_value": "120",
        "solution": {
            "steps": ["Half d1=12, other half=sqrt(169-144)=5, d2=10", "Area = (1/2)x24x10 = 120 cm2"],
            "trick": "Triplet 5-12-13! Area = (d1 x d2)/2"
        }
    },
    {
        "id": 33,
        "section": "G - Mensuration",
        "question": "Arc of circle radius 21cm, central angle 60 degrees. Arc length? (pi=22/7)",
        "options": {"a": "11cm", "b": "22cm", "c": "33cm", "d": "44cm"},
        "correct_answer": "b",
        "correct_value": "22 cm",
        "solution": {
            "steps": ["Arc = (60/360) x 2 x (22/7) x 21", "Arc = (1/6) x 132 = 22 cm"],
            "trick": "Arc = (angle/360) x 2*pi*r"
        }
    },
    {
        "id": 34,
        "section": "G - Mensuration",
        "question": "Right prism, hexagonal base side 6cm, height 10cm. Lateral SA?",
        "options": {"a": "360 cm2", "b": "300 cm2", "c": "240 cm2", "d": "420 cm2"},
        "correct_answer": "a",
        "correct_value": "360 cm2",
        "solution": {
            "steps": ["Perimeter = 6x6 = 36 cm", "LSA = 36x10 = 360 cm2"],
            "trick": "LSA = Perimeter of base x Height"
        }
    },
    {
        "id": 35,
        "section": "G - Mensuration",
        "question": "Right prism, equilateral triangle base side 10cm, height 12cm. Volume?",
        "options": {"a": "300root3 cm3", "b": "250root3 cm3", "c": "600 cm3", "d": "360 cm3"},
        "correct_answer": "a",
        "correct_value": "300root3 cm3",
        "solution": {
            "steps": ["Base area = (root3/4) x 100 = 25root3", "Volume = 25root3 x 12 = 300root3 cm3"],
            "trick": "V = Base Area x Height | Equilateral area = (root3/4)a^2"
        }
    },
    {
        "id": 36,
        "section": "H - Trigonometry",
        "question": "sin A + cos A = 4/3. Find tan A + cot A.",
        "options": {"a": "7/18", "b": "18/7", "c": "3/4", "d": "4/3"},
        "correct_answer": "b",
        "correct_value": "18/7",
        "solution": {
            "steps": ["(sinA+cosA)^2=16/9, sinAcosA=7/18", "tanA+cotA = 1/(sinAcosA) = 18/7"],
            "trick": "tanA+cotA = 1/(sinAcosA) shortcut"
        }
    },
    {
        "id": 37,
        "section": "H - Trigonometry",
        "question": "tan theta + cot theta = 2. Find tan^3 theta + cot^3 theta.",
        "options": {"a": "0", "b": "2", "c": "1", "d": "-1"},
        "correct_answer": "b",
        "correct_value": "2",
        "solution": {
            "steps": ["tan+cot=2 only when tan=cot=1, theta=45", "1^3 + 1^3 = 2"],
            "trick": "Minimum of tan+cot is 2, equality at theta=45"
        }
    },
    {
        "id": 38,
        "section": "H - Trigonometry",
        "question": "sec theta + tan theta = 3. Find tan theta.",
        "options": {"a": "3/4", "b": "4/3", "c": "1/3", "d": "5/3"},
        "correct_answer": "b",
        "correct_value": "4/3",
        "solution": {
            "steps": ["sec-tan = 1/3 (from identity)", "2tan = 3-1/3 = 8/3, tan = 4/3"],
            "trick": "sec+tan=3, so sec-tan=1/3. Add/subtract to find each"
        }
    },
    {
        "id": 39,
        "section": "H - Trigonometry",
        "question": "sin(5x - 40) = cos(5y + 40). Find x + y.",
        "options": {"a": "20", "b": "15", "c": "40", "d": "18"},
        "correct_answer": "d",
        "correct_value": "18 degrees",
        "solution": {
            "steps": ["sinA=cosB means A+B=90", "(5x-40)+(5y+40)=90", "5(x+y)=90, x+y=18"],
            "trick": "sinA=cosB implies A+B=90 degrees"
        }
    },
    {
        "id": 40,
        "section": "I - Circle & Geometry",
        "question": "PQ (diameter)=82cm, chord PS=80cm. Distance of PS from centre?",
        "options": {"a": "18cm", "b": "9cm", "c": "24cm", "d": "39cm"},
        "correct_answer": "b",
        "correct_value": "9 cm",
        "solution": {
            "steps": ["Radius=41, half chord=40", "Distance = sqrt(41^2-40^2) = sqrt(81) = 9cm"],
            "trick": "r^2 = d^2 + (chord/2)^2. Note 40-41 diff of squares trick"
        }
    },
    {
        "id": 41,
        "section": "I - Circle & Geometry",
        "question": "Chords AB & CD intersect inside circle at P. AP=10, PB=6, CP=4. Find PD.",
        "options": {"a": "12cm", "b": "15cm", "c": "18cm", "d": "14cm"},
        "correct_answer": "b",
        "correct_value": "15 cm",
        "solution": {
            "steps": ["AP x PB = CP x PD", "10 x 6 = 4 x PD", "PD = 60/4 = 15cm"],
            "trick": "Intersecting chords: AP x PB = CP x PD"
        }
    },
    {
        "id": 42,
        "section": "I - Circle & Geometry",
        "question": "Two circles radii 8cm & 6cm touch externally. Distance between centres?",
        "options": {"a": "2cm", "b": "10cm", "c": "14cm", "d": "12cm"},
        "correct_answer": "c",
        "correct_value": "14 cm",
        "solution": {
            "steps": ["External touch: distance = r1+r2", "Distance = 8+6 = 14cm"],
            "trick": "External: d=r1+r2 | Internal: d=|r1-r2|"
        }
    },
    {
        "id": 43,
        "section": "I - Circle & Geometry",
        "question": "Tangents PA & PB from external point P. PA=12cm. Find PB.",
        "options": {"a": "10cm", "b": "12cm", "c": "24cm", "d": "6cm"},
        "correct_answer": "b",
        "correct_value": "12 cm",
        "solution": {
            "steps": ["Tangents from external point are equal", "PB = PA = 12cm"],
            "trick": "Two tangents from same external point are always equal"
        }
    },
    {
        "id": 44,
        "section": "J - Number System",
        "question": "9-digit number 389x6378y divisible by 72. Find 6x + 7y.",
        "options": {"a": "16", "b": "28", "c": "64", "d": "32"},
        "correct_answer": "c",
        "correct_value": "64",
        "solution": {
            "steps": ["72=8x9. Div by 8: last 3 digits 78y, y=4 (784/8=98)", "Div by 9: digit sum 48+x divisible by 9, x=6", "6x+7y = 36+28 = 64"],
            "trick": "72=8x9. Apply both divisibility rules separately"
        }
    },
    {
        "id": 45,
        "section": "J - Number System",
        "question": "6-digit number 7002*4 divisible by 8. Smallest integer for *?",
        "options": {"a": "2", "b": "4", "c": "6", "d": "0"},
        "correct_answer": "a",
        "correct_value": "2",
        "solution": {
            "steps": ["Div by 8: check last 3 digits 2*4", "*=2: 224/8=28 correct"],
            "trick": "Divisibility by 8: only last 3 digits matter"
        }
    },
    {
        "id": 46,
        "section": "J - Number System",
        "question": "Which number is divisible by 9?",
        "options": {"a": "132490", "b": "553986", "c": "941201", "d": "350846"},
        "correct_answer": "b",
        "correct_value": "553986",
        "solution": {
            "steps": ["553986: 5+5+3+9+8+6 = 36", "36/9 = 4, divisible!"],
            "trick": "Div by 9: digit sum must be divisible by 9"
        }
    },
    {
        "id": 47,
        "section": "J - Number System",
        "question": "Largest 4-digit number divisible by 72?",
        "options": {"a": "9936", "b": "9960", "c": "9984", "d": "9992"},
        "correct_answer": "a",
        "correct_value": "9936",
        "solution": {
            "steps": ["9999/72 = 138.87", "138 x 72 = 9936"],
            "trick": "Divide largest number, take integer part, multiply back"
        }
    },
    {
        "id": 48,
        "section": "K - Percentage & Miscellaneous",
        "question": "Ramesh spends 60%. Income +30%, expenditure +20%. % increase in savings?",
        "options": {"a": "35%", "b": "45%", "c": "30%", "d": "50%"},
        "correct_answer": "b",
        "correct_value": "45%",
        "solution": {
            "steps": ["Income=100, savings=40", "New: income=130, expenditure=72, savings=58", "Increase = 18/40 x100 = 45%"],
            "trick": "Assume income=100, calculate new savings"
        }
    },
    {
        "id": 49,
        "section": "K - Percentage & Miscellaneous",
        "question": "Election: 12% didnt vote. Winner got 60% of total votes, beat by 1200. Total votes?",
        "options": {"a": "4000", "b": "3750", "c": "3570", "d": "5730"},
        "correct_answer": "b",
        "correct_value": "3750",
        "solution": {
            "steps": ["Winner=0.6N, Loser=0.28N", "Diff = 0.32N = 1200", "N = 3750"],
            "trick": "Winner-Loser = given margin, solve for N"
        }
    },
    {
        "id": 50,
        "section": "K - Percentage & Miscellaneous",
        "question": "Petrol +10%. Family uses 20L/month at Rs.100/L. Additional annual expenditure?",
        "options": {"a": "Rs.2000", "b": "Rs.2400", "c": "Rs.2200", "d": "Rs.1800"},
        "correct_answer": "b",
        "correct_value": "Rs.2,400",
        "solution": {
            "steps": ["Price increase = Rs.10/L", "Monthly extra = 20x10 = Rs.200", "Annual = 200x12 = Rs.2,400"],
            "trick": "Extra cost = quantity x price increase per unit x 12"
        }
    },
    {
        "id": 51,
        "section": "K - Percentage & Miscellaneous",
        "question": "Simplify (0.3-0.2)(0.3^2 + 0.3x0.2 + 0.2^2).",
        "options": {"a": "0.019", "b": "0.053", "c": "0.027", "d": "0.035"},
        "correct_answer": "a",
        "correct_value": "0.019",
        "solution": {
            "steps": ["Formula: a^3-b^3 = (a-b)(a^2+ab+b^2)", "= 0.3^3 - 0.2^3 = 0.027-0.008 = 0.019"],
            "trick": "Recognize a^3-b^3 pattern directly"
        }
    },
    {
        "id": 52,
        "section": "K - Percentage & Miscellaneous",
        "question": "If x^2-1, 2x, x^2+1 are sides of right triangle, which is hypotenuse?",
        "options": {"a": "x^2-1", "b": "x^2+1", "c": "x^2", "d": "2x"},
        "correct_answer": "b",
        "correct_value": "x^2+1",
        "solution": {
            "steps": ["x^2+1 is largest side", "Verify: (x^2+1)^2 = (x^2-1)^2 + (2x)^2"],
            "trick": "Largest side is hypotenuse. Verify with Pythagoras"
        }
    },
    {
        "id": 53,
        "section": "K - Percentage & Miscellaneous",
        "question": "Race: R gets 5m head start, beats S by 35m in 150m. S gets 25m start in 100m. Who wins?",
        "options": {"a": "S; 5.44m", "b": "S; 4.44m", "c": "R; 5.44m", "d": "R; 4.44m"},
        "correct_answer": "a",
        "correct_value": "S wins by 5.44m",
        "solution": {
            "steps": ["R:S speed ratio = 145:110 = 29:22", "Race2: S needs 75m, R needs 100m", "S wins by 5.44m"],
            "trick": "Find speed ratio from race 1, apply to race 2"
        }
    },
    {
        "id": 54,
        "section": "K - Percentage & Miscellaneous",
        "question": "Area of sector 88 cm2, angle 36 degrees. Find radius (pi=22/7).",
        "options": {"a": "3root70", "b": "5root70", "c": "root70", "d": "2root70"},
        "correct_answer": "d",
        "correct_value": "2root70",
        "solution": {
            "steps": ["(36/360) x (22/7) x r^2 = 88", "r^2 = 88x70/22 = 280", "r = 2root70"],
            "trick": "Sector area = (theta/360) x pi x r^2"
        }
    },
    {
        "id": 55,
        "section": "K - Percentage & Miscellaneous",
        "question": "If A:B=8:13, B:C=5:8, C:D=4:5, find A:B:C:D.",
        "options": {"a": "20:50:105:119", "b": "40:65:104:130", "c": "40:60:103:112", "d": "38:65:111:120"},
        "correct_answer": "b",
        "correct_value": "40:65:104:130",
        "solution": {
            "steps": ["A:B=40:65, B:C=65:104 (LCM method)", "D = 104x5/4 = 130", "A:B:C:D = 40:65:104:130"],
            "trick": "Chain ratio: make common element equal using LCM"
        }
    }
]


# ============================================
# STYLES
# ============================================
def get_styles():
    styles = {}
    styles['title'] = ParagraphStyle(
        'title', fontName='Helvetica-Bold', fontSize=11,
        textColor=colors.white, alignment=TA_CENTER,
        spaceAfter=2, spaceBefore=2
    )
    styles['section_hdr'] = ParagraphStyle(
        'section_hdr', fontName='Helvetica-Bold', fontSize=9,
        textColor=colors.white, alignment=TA_LEFT,
        spaceAfter=2, spaceBefore=2, leftIndent=4
    )
    styles['question'] = ParagraphStyle(
        'question', fontName='Helvetica-Bold', fontSize=8,
        textColor=colors.black, spaceAfter=3,
        spaceBefore=3, leftIndent=2
    )
    styles['option'] = ParagraphStyle(
        'option', fontName='Helvetica', fontSize=7.5,
        textColor=colors.black, spaceAfter=1, leftIndent=4
    )
    styles['answer'] = ParagraphStyle(
        'answer', fontName='Helvetica-Bold', fontSize=8,
        textColor=colors.HexColor('#8B6914'),
        spaceAfter=2, leftIndent=2
    )
    styles['solution'] = ParagraphStyle(
        'solution', fontName='Helvetica-Oblique', fontSize=7,
        textColor=colors.HexColor('#444444'),
        spaceAfter=1, leftIndent=4
    )
    styles['info'] = ParagraphStyle(
        'info', fontName='Helvetica-Bold', fontSize=8,
        textColor=colors.black, alignment=TA_LEFT
    )
    styles['inst'] = ParagraphStyle(
        'inst', fontName='Helvetica', fontSize=7.5,
        textColor=colors.black
    )
    return styles


# ============================================
# QUESTION CELL
# ============================================
def make_cell(q, styles):
    content = []
    star = "* " if q['id'] <= 18 else "* "
    content.append(Paragraph(
        f"{star}Q{q['id']}. {q['question']}",
        styles['question']
    ))
    opts = list(q['options'].items())
    if len(opts) >= 2:
        content.append(Paragraph(
            f"(a) {opts[0][1]}     (b) {opts[1][1]}",
            styles['option']
        ))
    if len(opts) >= 4:
        content.append(Paragraph(
            f"(c) {opts[2][1]}     (d) {opts[3][1]}",
            styles['option']
        ))
    content.append(Paragraph(
        f"Ans: ({q['correct_answer']}) {q['correct_value']}",
        styles['answer']
    ))
    sol = " | ".join(q['solution']['steps'])
    if len(sol) > 150:
        sol = sol[:150] + "..."
    content.append(Paragraph(sol, styles['solution']))
    return content


# ============================================
# GROUP BY SECTION
# ============================================
def group_sections(data):
    sections = {}
    order = []
    for q in data:
        s = q['section']
        if s not in sections:
            sections[s] = []
            order.append(s)
        sections[s].append(q)
    return sections, order


# ============================================
# BUILD PDF
# ============================================
def build_pdf(data, filename="SSC_Maths_TwoColumn.pdf"):
    doc = SimpleDocTemplate(
        filename, pagesize=A4,
        rightMargin=0.8*cm, leftMargin=0.8*cm,
        topMargin=1.2*cm, bottomMargin=1.2*cm
    )
    styles = get_styles()
    story = []
    W = A4[0] - 1.6*cm

    # --- TITLE ---
    t = Table([[Paragraph(
        "SSC Selection Post — Maths Repeated Concepts Practice Sheet",
        styles['title']
    )]], colWidths=[W])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#1a3a5c')),
        ('TOPPADDING', (0,0), (-1,-1), 7),
        ('BOTTOMPADDING', (0,0), (-1,-1), 7),
    ]))
    story.append(t)
    story.append(Spacer(1, 0.15*cm))

    # --- INFO ROW ---
    info = Table([[
        Paragraph("<b>Time Allowed:</b> 3 Hrs 20 Min", styles['info']),
        Paragraph("<b>Total Questions:</b> 55", styles['info']),
        Paragraph("<b>Maximum Marks:</b> 220", styles['info']),
    ]], colWidths=[W/3]*3)
    info.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 0.5, colors.grey),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f0f0f0')),
    ]))
    story.append(info)
    story.append(Spacer(1, 0.1*cm))

    # --- INSTRUCTIONS ---
    inst = Table([[Paragraph(
        "<b>Instructions:</b> +4 for correct | -1 for wrong | "
        "* = appeared 5+ times | # = appeared 3-4 times across SSC papers",
        styles['inst']
    )]], colWidths=[W])
    inst.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#FFA500')),
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#FFFBF0')),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(inst)
    story.append(Spacer(1, 0.25*cm))

    # --- SECTIONS + QUESTIONS ---
    sections, order = group_sections(data)
    col_w = (W - 0.2*cm) / 2

    for sec in order:
        qs = sections[sec]

        # Section Header
        sh = Table([[Paragraph(
            f"SECTION {sec} [* 5+ times]",
            styles['section_hdr']
        )]], colWidths=[W])
        sh.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#1a5276')),
            ('TOPPADDING', (0,0), (-1,-1), 5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 5),
            ('LEFTPADDING', (0,0), (-1,-1), 6),
        ]))
        story.append(sh)
        story.append(Spacer(1, 0.1*cm))

        # 2-column question pairs
        for i in range(0, len(qs), 2):
            left = make_cell(qs[i], styles)
            right = make_cell(qs[i+1], styles) if i+1 < len(qs) else [Paragraph("", styles['question'])]

            row = Table(
                [[left, right]],
                colWidths=[col_w, col_w]
            )
            row.setStyle(TableStyle([
                ('BOX', (0,0), (0,0), 0.4, colors.HexColor('#bbbbbb')),
                ('BOX', (1,0), (1,0), 0.4, colors.HexColor('#bbbbbb')),
                ('BACKGROUND', (0,0), (-1,-1), colors.white),
                ('VALIGN', (0,0), (-1,-1), 'TOP'),
                ('TOPPADDING', (0,0), (-1,-1), 5),
                ('BOTTOMPADDING', (0,0), (-1,-1), 5),
                ('LEFTPADDING', (0,0), (-1,-1), 5),
                ('RIGHTPADDING', (0,0), (-1,-1), 5),
                ('LINEAFTER', (0,0), (0,-1), 0.4, colors.HexColor('#bbbbbb')),
            ]))
            story.append(row)
            story.append(Spacer(1, 0.1*cm))

        story.append(Spacer(1, 0.2*cm))

    doc.build(story)
    print(f"PDF ready: {filename}")


# ============================================
# RUN
# ============================================
build_pdf(data)
