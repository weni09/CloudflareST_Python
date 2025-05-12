import platform
import struct
from enum import Enum


# ------------------------
# 系统类型枚举
# ------------------------
class OperatingSystem(Enum):
    WINDOWS = "Windows"
    LINUX = "Linux"
    DARWIN = "Darwin"
    JAVA = "Java"
    CYGWIN = "CYGWIN"
    MSYS = "MSYS"
    AIX = "AIX"
    FREEBSD = "FreeBSD"
    OPENBSD = "OpenBSD"
    NETBSD = "NetBSD"
    SUNOS = "SunOS"
    HPUX = "HP-UX"
    UNKNOWN = "Unknown"


# ------------------------
# 架构枚举
# ------------------------
class CPUArchitecture(Enum):
    X86 = "x86"
    X86_64 = "x86_64"
    AMD64 = "AMD64"
    ARM = "arm"
    ARM64 = "aarch64"
    ARMv7 = "armv7l"
    ARMv6 = "armv6l"
    MIPS = "mips"
    MIPS64 = "mips64"
    PPC64LE = "ppc64le"
    RISCV64 = "riscv64"
    SPARC = "sparc"
    UNKNOWN = "unknown"


class SystemInfo:
    @staticmethod
    def normalize_arch(machine_str: str) -> CPUArchitecture:
        arch_map = {
            "x86_64": CPUArchitecture.X86_64,
            "AMD64": CPUArchitecture.X86_64,
            "i386": CPUArchitecture.X86,
            "i686": CPUArchitecture.X86,
            "arm": CPUArchitecture.ARM,
            "armv7l": CPUArchitecture.ARMv7,
            "armv6l": CPUArchitecture.ARMv6,
            "aarch64": CPUArchitecture.ARM64,
            "mips": CPUArchitecture.MIPS,
            "mips64": CPUArchitecture.MIPS64,
            "ppc64le": CPUArchitecture.PPC64LE,
            "riscv64": CPUArchitecture.RISCV64,
            "sparc": CPUArchitecture.SPARC,
        }
        return arch_map.get(machine_str, CPUArchitecture.UNKNOWN)

    @staticmethod
    def normalize_system(sys_name: str) -> OperatingSystem:
        try:
            return OperatingSystem(sys_name)
        except ValueError:
            return OperatingSystem.UNKNOWN

    # ------------------------
    # 主函数：获取系统信息
    # ------------------------
    def get_system_info(self) -> dict:
        raw_system = platform.system()
        raw_machine = platform.machine()

        return {
            "system": self.normalize_system(raw_system).value,
            "release": platform.release(),
            "version": platform.version(),
            "architecture": self.normalize_arch(raw_machine).value,
            "python_bits": f"{struct.calcsize('P') * 8}-bit",
            "raw_system": raw_system,
            "raw_machine": raw_machine,
        }
