# ==============================CS-199==================================
# FILE:			MyAI.py
#
# AUTHOR: 		Justin Chung
#
# DESCRIPTION:	This file contains the MyAI class. You will implement your
#				agent in this file. You will write the 'getAction' function,
#				the constructor, and any additional helper functions.
#
# NOTES: 		- MyAI inherits from the abstract AI class in AI.py.
#
#				- DO NOT MAKE CHANGES TO THIS FILE.
# ==============================CS-199==================================

from AI import AI
from Action import Action


class MyAI( AI ):

	def __init__(self, rowDimension, colDimension, totalMines, startX, startY):

		########################################################################
		#							YOUR CODE BEGINS						   #
		########################################################################
		self.rowDimension = rowDimension
		self.colDimension = colDimension
		self.totalMines = totalMines
		
		# Creating the persistent board.
		# -1 = covered
		# -2 = marked (flagged)
		# -3 = queued to uncover
		# 0-8 = uncovered with that many neighboring mines
		self.board = []
		for i in range(colDimension):
			self.board.append([])
			for j in range(rowDimension):
				self.board[i].append(-1)

		# Storing previous tiles' coordinates and action. Initial action is an uncover at tile (startX, startY).
		self.prevAction = AI.Action.UNCOVER
		self.prevX = startX
		self.prevY = startY
		
		self.actionQueue = []
		self.uncoveredTiles = 0
		########################################################################
		#							YOUR CODE ENDS							   #
		########################################################################

		
	def getAction(self, number: int) -> "Action Object":

		########################################################################
		#							YOUR CODE BEGINS						   #
		########################################################################
		
		# Update board if tile was uncovered. First priority to avoid taking action on an outdated board.
		if self.prevAction == AI.Action.UNCOVER and number >= 0:
			if self.board[self.prevX][self.prevY] < 0:
				self.board[self.prevX][self.prevY] = number
				self.uncoveredTiles += 1

		# Check for win condition (uncovering all safe tiles).
		if self.uncoveredTiles == (self.colDimension * self.rowDimension) - self.totalMines:
			return Action(AI.Action.LEAVE)

		# If action in queue, execute it.
		if self.actionQueue:
			return self.executeAction()

		# If the queue is empty, scan the board and apply Single-Point Rules of Thumb.
		for i in range(self.colDimension):
			for j in range(self.rowDimension):
				label = self.board[i][j]

				if label >= 0:
					coveredNeighbors = []
					markedNeighbors = 0

					# Gather all valid neighbors for the current tile
					for relativeX in [-1, 0, 1]:
						for relativeY in [-1, 0, 1]:
							# Skip loop if the neighbor is the current tile itself.
							if relativeX == 0 and relativeY == 0: continue
							# Otherwise, neighbor's coordinates are (i + relativeX, j + relativeY).
							neighborX, neighborY = i + relativeX, j + relativeY
							
							# Check boundary constraints
							if 0 <= neighborX < self.colDimension and 0 <= neighborY < self.rowDimension:
								state = self.board[neighborX][neighborY]
								if state == -1 or state == -3:
									coveredNeighbors.append((neighborX, neighborY))
								elif state == -2:
									markedNeighbors += 1

					# Effective Label = NumUnmarkedNeighbors = Label(x) - NumMarkedNeighbors(x)
					effectiveLabel = label - markedNeighbors

					# 1st Rule: If EffectiveLabel == 0, all covered neighbors are safe to uncover.
					if effectiveLabel == 0 and len(coveredNeighbors) > 0:
						for neighborX, neighborY in coveredNeighbors:
							if self.board[neighborX][neighborY] == -1:
								self.board[neighborX][neighborY] = -3 # Mark as queued to uncover
								self.actionQueue.append((AI.Action.UNCOVER, neighborX, neighborY))
						
						if self.actionQueue:
							return self.executeAction()

					# 2nd Rule: If EffectiveLabel == NumUnmarkedNeighbors, all covered neighbors are mines and can be flagged.
					if effectiveLabel == len(coveredNeighbors) and len(coveredNeighbors) > 0:
						for neighborX, neighborY in coveredNeighbors:
							if self.board[neighborX][neighborY] == -1 or self.board[neighborX][neighborY] == -3:
								self.board[neighborX][neighborY] = -2 # Mark as flagged
								self.actionQueue.append((AI.Action.FLAG, neighborX, neighborY))
						
						if self.actionQueue:
							return self.executeAction()

		# If no rules apply and the queue is empty, we have to guess (randomly uncover a covered tile).
		for i in range(self.colDimension):
			for j in range(self.rowDimension):
				if self.board[i][j] == -1:
					self.board[i][j] = -3
					self.prevAction = AI.Action.UNCOVER
					self.prevX = i
					self.prevY = j
					return Action(AI.Action.UNCOVER, i, j)

	# Helper function to process queue.
	def executeAction(self):
		action, x, y = self.actionQueue.pop(0)
		self.prevAction = action
		self.prevX = x
		self.prevY = y
		return Action(action, x, y)

		########################################################################
		#							YOUR CODE ENDS							   #
		########################################################################