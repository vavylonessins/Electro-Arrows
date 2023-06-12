import ctypes


u64 = "ctypes.c_ulonglong"
u32 = "ctypes.c_ulong"
u16 = "ctypes.c_ushort"
u8  = "ctypes.c_ubyte"

i64 = "ctypes.c_longlong"
i32 = "ctypes.c_long"
i16 = "ctypes.c_short"
i8  = "ctypes.c_byte"

string = "ctypes.c_wchar_p"

true = 1
false = 0
null = 0


START_CLASS_CODE = """

class class_name:

"""

INIT_FUNC_CODE = """

	def __init__(self, args):

"""

INIT_FIELD_CODE = """

		if type(field_name) != field_type:
			raise TypeError(f"field {field_name} should be of type {field_type.__class__.__name__}")
		self.field_name = field_name

"""


builtin_attributes = [
	'__new__',
	'__repr__',
	'__hash__',
	'__str__',
	'__getattribute__',
	'__setattr__',
	'__delattr__',
	'__lt__',
	'__le__',
	'__eq__',
	'__ne__',
	'__gt__',
	'__ge__',
	'__init__',
	'__reduce_ex__',
	'__reduce__',
	'__subclasshook__',
	'__init_subclass__',
	'__format__',
	'__sizeof__',
	'__dir__',
	'__class__',
	'__doc__'
]


def struct(**d):
	code = START_CLASS_CODE
	ind = 1

	# init function #
	init_fn = INIT_FUNC_CODE.replace("args", ", ".join(tuple(d.keys())))
	ind += 1

	for f in d.keys():
		t = d[f]
		print(f, t)
		init_fn += INIT_FIELD_CODE.replace("field_name", f).replace("field_type", t)

	lcl = glb = {}

	exec(code+init_fn, lcl, glb)

	return glb["class_name"]


if __name__ == '__main__':

	test_type = struct(
		my_size = u64,
		is_3d = "bool",
		x = i32,
		y = i32,
		flags_and_layers_num = u16,
		layers = string
	)

	# test_obj_1 = test_type.from_bytes('\u0967\uf58d ... \u0967\uf58d')

	test_obj_2 = test_type(
		82,
		true,
		-15,
		10,
		2<<12&1,
		'\u0967\uf58d ... \u0967\uf58d'
	)


