connections = [
	[A.output, B.inputs[0]],
	[A.output, wires[43]],
	[A.output, wires[43]],
	[wires[43], wires[8]]
]

schema.wires = [<Wire1>,<Wire2>,...]

class Wire:
	# Nodes are grid points
	# Segments are pairs of grid points (nodes). A segment is a line that connects two points.
	segments = [
		((0,0),(0,2)),
		((0,2),(1,2)),
		((1,1),(1,2)),
		((1,2),(1,3)),
		((1,3),(2,3))
	]

Grid
	Schema
		Element
			Port
			Wire
			Annotation
				Text
			Circuit

'''
Grid: 		Interface between user events and simulation. Captures mouse/keyboard
			events, interprets them and sends and modifies schema if needed.
Schema: 	(Or simulation) takes care of the actual logic and simulation. Holds
			information of all elements, wires etc.
Element: 	Port, Wire, Annotation and everything that goes to the grid, is
			a special case of an element. Element always has grid coordinates.
Port: 		An elementary gate that takes one or more inputs and converts them
			to one output.
Wire: 		Series of lines on the grid that connects with elements. One wire
			always has a deterministic state (0/1) and so have all inputs that
			are connected to it.


'''


# When an event occurs on the schema (e.g. delete a wire using mouse),
# update connections concerning that element:
grid.state = [
	activeElement: <Wire4>
]

class Scigol:
	...
	def handleRightClick(self):
		mpos = pg.mouse.get_pos()
		element = self.checkMouseHits(mpos)
		if element:
			self.openContextMenu()

	def checkMouseHits(self, mpos):
		grid = self.currentTab
		for el in grid.elements:
			if mpos.x >= el.dims.x-el.dims.width and mpos.x <= el.dims.x+el.dims.width ...:
				return el
		return None


class Grid:
		...
		def deleteElement(self, element):
			element.beforeDestroy()		# removes connections from scheme etc.
			self.elements
