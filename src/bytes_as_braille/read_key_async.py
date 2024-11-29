import asyncio
import sys
import termios
import tty
import select

async def read_key():
	"""
	Asynchronously read a single keypress.
	
	NOTE: cannot be replaced by aioinput.ainput
	TODO: will not work if [esc] is pressed!
	"""
	def blocking_read_key():
		fd = sys.stdin.fileno()
		old_settings = termios.tcgetattr(fd)
		try:
			tty.setraw(fd)
			while True:
				if select.select([sys.stdin], [], [], 0.1)[0]:	# wait at most 100ms for buffer to contain something
					char = sys.stdin.read(1)  # Read the first character
	
					# Handle special cases and escape sequences
					if char == '\x1b':  # Start of an escape sequence or standalone Esc
						next_chars = sys.stdin.read(3)  # Attempt to read up to 3 more characters
						return char + next_chars
					else:
						return char
		finally:
			termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

	return await asyncio.to_thread(blocking_read_key)

# Example usage
async def main():
	print("Press any key (Ctrl+C to exit):")
	try:
		while True:
			key = await read_key()
			print(f"You pressed: {key}")
	except KeyboardInterrupt:
		print("\nExiting gracefully.")

if __name__ == '__main__':
	asyncio.run(main())

