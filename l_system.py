import PIL.ImageDraw as ImageDraw,PIL.Image as Image, PIL.ImageShow as ImageShow
import math

class Point(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def distance(self, other):
        dx = self.x - other.x
        dy = self.y - other.y
        return math.sqrt(dx**2 + dy**2)

    def clone(self):
    	return Point(self.x, self.y)

    def __str__(self):
        return "Point(%s,%s)"%(self.x, self.y)

class XTurtle:
    def __init__(self, Origine, Angle, Len):
        self.O = Origine.clone()
        self.Dest = Origine.clone()
        self.len = Len
        self.angle = Angle
        self.config(0, self.len)

    def clone(self):
    	return XTurtle(self.O.clone(), self.angle, self.len)

    def normalize_angle(self):
    	two_pi = math.pi * 2
    	normalized = self.angle % (two_pi)
    	normalized = (normalized + (two_pi)) % (two_pi)
    	if (normalized <= math.pi):
    		self.angle = normalized
    	else:
    		self.angle = normalized - (math.pi * 2)

    def draw_line(self, draw, r, g, b):
        draw.line((self.O.x, self.O.y, self.Dest.x, self.Dest.y), fill=(r,g,b))
        self.O = self.Dest.clone()
        self.config(0, self.len)

    def config(self, _angle, _len):
    	self.len = _len
    	self.angle = self.angle + _angle
    	self.normalize_angle()
    	self.Dest.x = self.O.x + _len * math.cos(self.angle)
    	self.Dest.y = self.O.y - _len * math.sin(self.angle)

    def __str__(self):
    	return "turtule(%s,%s)"%(self.O, self.Dest)

class YTurtle:
	def __init__(self, Origine, Angle, len):
		trtl = XTurtle(Origine, Angle, len)
		self.history = []
		self.history.append(trtl)

	def drawLine(self, draw, r, g, b):
		self.history[len(self.history) - 1].draw_line(draw, r, g, b)

	def config(self, _angle, _len):
		self.history[len(self.history) - 1].config(_angle, _len)

	def push(self):
		_trtl = self.history[len(self.history) - 1].clone()
		self.history.append(_trtl)

	def pop(self):
		self.history.pop(len(self.history) - 1)

class Rule:
	def __init__(self, _value, _exp):
		self.value = _value
		self.exp = _exp

def gen_exp(axiom, rules, depth):
    exp = ""
    tmp = axiom

    for i in range(len(tmp)):
        flag = False
        for k in range(len(rules)):
            if (tmp[i] == rules[k].value):
                exp = exp + rules[k].exp
                flag = True
                break;
        if (not flag):
            exp = exp + tmp[i]
    return (gen_exp(exp, rules, depth - 1) if depth > 1 else exp)

def draw_exp(draw, turtle, full_exp, _angle, _len):
    new_expression = full_exp
    for i in range(len(new_expression)):
        if (new_expression[i] == 'F'):
            turtle.drawLine(draw, 255, 255, 255)
        elif (new_expression[i] == '-'):
    	    turtle.config(-_angle, _len)
        elif(new_expression[i] == '+'):
    	    turtle.config(_angle, _len)
        elif(new_expression[i] == '['):
    	    turtle.push()
        elif(new_expression[i] == ']'):
    	    turtle.pop()


def l_system(draw, axiom, arr_rules, depth, _angle, _origine, _len):
	turtle = YTurtle(_origine, math.pi / 2, _len)
	exp = gen_exp(axiom, arr_rules, depth)
	print("Expression ready")
	draw_exp(draw, turtle, exp, _angle, _len)

W = 5000
H = 5000

o = Point(W/2, H)

im = Image.new("RGB", (W,H))
draw = ImageDraw.Draw(im)

rules = []

axiom = "F+F+F+F"
rule1 = Rule("F", "FF+F-F+F+FF")

rules.append(rule1)
#rules.append(rule2)
angle = 90 * math.pi / 180

l_system(draw, axiom, rules, 5, angle, Point(W/2, H/2), 40)

im.show()
im.save('plant1.png')
