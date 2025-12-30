from src.shell import Shell
from src.kernel import Kernel

shell = Shell()
kernel = Kernel(shell)

kernel.loop()