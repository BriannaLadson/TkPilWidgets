from tkinter import Canvas
from PIL import Image, ImageDraw, ImageTk

class TkRadialProgress(Canvas):
	def __init__(self, parent, value=0, max_value=100, **kwargs):
		self.options = {
			"size": 150,
			"bg": "white",
			"background_color": "#e6e6e6",  # renamed
			"progress_color": "#4caf50",    # renamed
			"border_thickness": 12,
			"outline_color": "black",
			"outline_thickness": 2,
			"text_color": "black",
			"font": ("Arial", 12, "bold"),
			"start_angle": 90,
			"direction": "counterclockwise",
			"show_percent_text": True
		}

		self.auto_increment = kwargs.pop("auto_increment", False)
		self.increment_step = kwargs.pop("increment_step", 1)
		self.increment_interval = kwargs.pop("increment_interval", 100)
		self.loop = kwargs.pop("loop", True)

		self.options.update(kwargs)

		super().__init__(
			parent,
			width=self.options["size"],
			height=self.options["size"],
			bg=self.options["bg"],
			highlightthickness=0
		)

		self.value = value
		self.max_value = max_value
		self.image = None

		self.bind("<Configure>", self.redraw)

		if self.auto_increment:
			self._start_auto_increment()

	def config(self, **kwargs):
		self.options.update(kwargs)
		if "size" in kwargs:
			self.config(width=self.options["size"], height=self.options["size"])
		self.redraw()

	def set(self, value):
		self.value = max(0, min(value, self.max_value))
		self.redraw()
		
	def set_size(self, new_size):
		self.options["size"] = new_size
		
		self.config(width=new_size, height=new_size)
		
		self.redraw()

	def _start_auto_increment(self):
		if self.auto_increment:
			self.set(self.value + self.increment_step)
			if self.value >= self.max_value:
				if self.loop:
					self.set(0)
				else:
					return
			self.after(self.increment_interval, self._start_auto_increment)

	def redraw(self, event=None):
		size = self.options["size"]
		scale = 4
		full_size = size * scale
		img = Image.new("RGB", (full_size, full_size), self.options["bg"])
		draw = ImageDraw.Draw(img)

		center = full_size // 2
		border_thickness = self.options["border_thickness"] * scale
		outline_thickness = self.options["outline_thickness"] * scale
		radius = center - outline_thickness

		user_angle = self.options["start_angle"] % 360
		pillow_start = -user_angle
		angle = 360 * (self.value / self.max_value)

		if self.options["direction"] == "clockwise" or self.value == 0:
			end_angle = pillow_start + angle
			
			ring_color = self.options["background_color"]
			progress_color = self.options["progress_color"]
			
		else:
			end_angle = pillow_start - angle
			
			ring_color = self.options["progress_color"]
			progress_color = self.options["background_color"]

		# Full ring using background color
		draw.arc(
			[center - radius, center - radius, center + radius, center + radius],
			start=0,
			end=360,
			fill=ring_color,
			width=border_thickness
		)

		# Overlay arc using progress color
		draw.arc(
			[center - radius, center - radius, center + radius, center + radius],
			start=pillow_start,
			end=end_angle,
			fill=progress_color,
			width=border_thickness
		)

		# Outer and inner outlines
		if self.options["outline_thickness"] > 0:
			draw.ellipse(
				[center - radius, center - radius, center + radius, center + radius],
				outline=self.options["outline_color"],
				width=outline_thickness
			)
			inner_radius = radius - border_thickness
			if inner_radius > 0:
				draw.ellipse(
					[center - inner_radius, center - inner_radius,
					center + inner_radius, center + inner_radius],
					outline=self.options["outline_color"],
					width=outline_thickness
				)

		# Resize and show on canvas
		img = img.resize((size, size), Image.LANCZOS)
		self.image = ImageTk.PhotoImage(img)
		self.delete("all")
		canvas_width = self.winfo_width()
		canvas_height = self.winfo_height()
		min_size = min(canvas_width, canvas_height)
		self.create_image(canvas_width // 2, canvas_height // 2, image=self.image)

		# Progress text
		if self.options["show_percent_text"]:
			percent = int((self.value / self.max_value) * 100)
			self.create_text(
				size // 2, size // 2,
				text=f"{percent}%",
				fill=self.options["text_color"],
				font=self.options["font"]
		 )

# Demo
if __name__ == "__main__":
	from tkinter import Tk

	root = Tk()
	root.title("TkRadialProgress Demo")

	progress = TkRadialProgress(
		root,
		value=100,
		max_value=100,
		size=300,
		progress_color="#f44336",
		background_color="yellow",
		border_thickness=30,
		outline_thickness=0,
		outline_color="#000",
		start_angle=90,
		direction="clockwise",
		show_percent_text=True,
		auto_increment=False,
		increment_step=1,
		increment_interval=100,
		loop=True
	)
	progress.pack(padx=20, pady=20)

	root.mainloop()
