from enum import Enum, Flag
from typing import *
from typing import BinaryIO
import struct
import numpy as np


class SenseX1000Base(object):
    USB_VID: int = 0x1FC9
    USB_PID: int = 0x8271

    class IPVersion(Enum):
        IPV4 = 4
        IPV6 = 6

    class IPv4AutoconfStatus(Enum):
        OFF = 0
        PROBING = 1
        ANNOUNCING = 2
        BOUND = 3

    class IPv6AutoconfStatus(Enum):
        NOTIMPLEMENTED = 0

    class IPv4DHCPStatus(Enum):
        OFF = 0
        REQUESTING = 1
        INIT = 2
        REBOOTING = 3
        REBINDING = 4
        RENEWING = 5
        SELECTING = 6
        INFORMING = 7
        CHECKING = 8
        PERMANENT = 9
        BOUND = 10
        RELEASING = 11
        BACKINGOFF = 12

    class IPv6DHCPStatus(Enum):
        NOTIMPLEMENTED = 0

    class PowerLevel(Enum):
        UNKNOWN = 0
        LOW = 1
        MEDIUM = 2
        HIGH = 3
        AUTO = 4

    class RadarState(Enum):
        OFF = 0
        STANDBY = 11
        IDLE = 12
        BUSY = 15
        DETECTFAIL = 40
        MAGICFAIL = 45

    # Enums for CONTrol subsystem
    class RampMode(Enum):
        """Ramp mode used with CONTrol:RADAR:MPLL:RMODe"""
        SINGLE = 0
        """Perform single ramps on each trigger"""
        DOUBLE = 1
        """Perform double ramps on each trigger"""
        ALTERNATING = 2
        """Perform alternating ramps on each trigger"""

    class ChannelCoupling(Enum):
        """Frontend coupling of receive channel used with CONTrol:RADAR:FRONtend:CHANnel#:COUPling"""
        GND = 0
        """Set GND channel coupling"""
        DC = 1
        """Set DC channel coupling"""
        AC = 2
        """Set AC channel coupling (R^2 compensation)"""

    class ChannelForce(Enum):
        """Frontend channel force used with CONTrol:RADAR:FRONtend:CHANnel#:FORCe"""
        NONE = 0
        """Do not force channel state"""
        ON = 1,
        """Force channel to always-on"""
        OFF = 2
        """Force channel to always-off"""

    # Enums for SENSe subsystem
    class FrequencyMode(Enum):
        """Frequency mode used with SENSe:FREQuency:MODE"""
        CW = 0
        """Operate in continuous wave mode on a single frequency (aka zero-span)"""
        SWEEP = 1
        """Operate in swept mode (normal)"""

    class SweepDirection(Enum):
        """Sweep direction used with SENSe:SWEep:DIRection"""
        DOWN = -1
        """Sweep slope of (first) sweep is down"""
        UP = 1
        """Sweep slope of (first) sweep is up"""

    class SweepMode(Enum):
        """Sweep mode used with SENSe:SWEep:MODE"""
        NORMAL = 0
        """Sweep slope is constant with jump back to start frequency at the end of sweep"""
        ALTERNATING = 1
        """Sweep slope is alternating in consecutive sweeps"""

    class RefOscSource(Enum):
        """Reference Oscillator source used with SENSe:ROSCillator:SOURCE"""
        NONE = 0
        """No reference oscillator, free running"""
        INTERNAL = 1
        """Internal reference oscillator source (if available)"""
        EXTERNAL = 2
        """External reference oscillator source (if available)"""

    class RefOscStatus(Enum):
        """Status of reference oscillator used with SENSe:ROSCillator:STATus"""
        OFF = 0
        """Reference oscillator PLL is disabled, i.e. during power-off"""
        HOLDOVER = 1
        """Reference oscillator PLL is in holdover mode (source lost)"""
        LOCKING = 2
        """Reference oscillator PLL is trying to lock to selected reference"""
        LOCKED = 3
        """Reference oscillator PLL is locked to selected reference"""
        LOCK = 3
        """Deprecated"""

    # Enums for TRIGger subsystem
    class TrigSource(Enum):
        """Trigger source used with TRIGger:SOURce"""
        IMMEDIATE = 0
        """A trigger will commence immediately after the device is initiated"""

    # Data type information container
    class AcqDTypeInfo(NamedTuple):
        min: Union[int, complex]
        max: Union[int, complex]
        mag: int
        np: np.dtype

    # Enums/Flags for AcquisitionHeader
    class AcqDType(Enum):
        """Acquisition Datatype used in acquisition header"""
        S16RLE = 0
        """Signed 16 bit (real), little endian"""
        S16RILE = 4
        """Signed 16 bit (real, imaginary), little endian"""

        @property
        def info(self) -> 'SenseX1000Base.AcqDTypeInfo':
            """Information about data type as AcqDTypeInfo object"""
            return {
                self.S16RLE.value: SenseX1000Base.AcqDTypeInfo(
                    min=-32768, max=32767, mag=32768, np=np.dtype('<i2')),
                self.S16RILE.value: SenseX1000Base.AcqDTypeInfo(
                    min=-32768-32768j, max=32767+32767j, mag=32768, np=np.dtype([('re', '<i2'), ('im', '<i2')]))
            }[self.value]

    class AcqFlags(Flag):
        """Acquisition flags used in acquisition header"""
        SDOMAIN = 1 << 4
        """Sweep Domain data"""
        RDOMAIN = 1 << 5
        """Range Domain data"""
        DIRECTION = 1 << 8
        """Falling (0) or rising (1) slope of first sweep in acquisition"""
        ALTERNATING = 1 << 9
        """Constant (0) or alternating (1) sweep slope for multiple sweep acquisitions"""

    class AcqHeader(NamedTuple):
        """Class representing the header prepended to every acquisition"""
        # header fields as named tuple entries.
        # Note that the order of these entries must match the binary header format
        header_length: int
        """Binary header size"""
        header_id: int
        """Binary header identifier"""
        header_version: int
        """Binary header version"""
        flags: int
        """Acquisition flags as integer"""
        bytes_total: int
        """Total number of bytes in acquisition"""
        sweep_count: int
        """Number of sweeps in acquisition"""
        trace_mask: int
        """Bitmask of enabled traces in acquisition"""
        data_points: int
        """Number of points per trace"""
        data_size: int
        """Size of datatype in bytes"""
        data_type: int
        """Datatype identifier"""

        @classmethod
        def struct(cls) -> struct.Struct:
            # Return a Python struct object for parsing the binary header into the named tuple
            return struct.Struct('<HBBLLLLLBBxxxxxx')

        @classmethod
        def version(cls) -> int:
            # Return version supported by this NamedTuple
            return 1

        @classmethod
        def from_stream(cls, stream: BinaryIO) -> 'SenseX1000Base.AcqHeader':
            # Get struct object, unpack binary data and create an AcqHeader object
            s = cls.struct()
            buffer = stream.read(s.size)
            data = s.unpack(buffer)
            header = SenseX1000Base.AcqHeader(*data)

            assert header.header_version == cls.version(), "Unsupported Acquisition Header Version {} (expected: {})".format(header.header_version, cls.version())

            return header

        @property
        def trace_list(self) -> List[int]:
            """List of traces enabled in this acquisition"""
            mask = self.trace_mask
            lst = []
            i = 0
            while mask > 0:
                if mask & (1 << i):
                    lst += [i]
                    mask = mask & ~(1 << i)
                i += 1
            return lst

        @property
        def trace_count(self) -> int:
            """Number of traces enabled in this acquisition"""
            return len(self.trace_list)

        @property
        def acq_dtype(self) -> 'SenseX1000Base.AcqDType':
            """Acqusition data type as AcqDType object"""
            return SenseX1000Base.AcqDType(self.data_type)

        @property
        def acq_flags(self) -> 'SenseX1000Base.AcqFlags':
            """Acquisition flags as AcqFlags object"""
            return SenseX1000Base.AcqFlags(self.flags)

    class AcqData(object):
        """Class representing an acquisition data object holding data for one or more consecutive sweeps"""
        header: 'SenseX1000Base.AcqHeader'
        """Copy of the acquisition header to which this data container belongs"""
        array: np.ndarray
        """Acquisition data as numpy array with shape N_sweeps x N_traces x N_points"""
        n_sweeps: int
        """Number of sweeps in this container"""
        n_traces: int
        """Number of traces per sweep"""
        n_points: int
        """Number of points per trace"""
        trace_list: list
        """Mapping of the trace index in the data array to the respective trace number"""
        seq_nums: list
        """List of sweep sequence numbers with respect to entire acquisition for each sweep in data array"""
        sweep_dir: int
        """Direction of first sweep in acquisition as sign value (-1, +1)"""
        sweep_dirs: list
        """List of sweep directions for each sweep in data array as sign value (-1, +1)"""

        @classmethod
        def from_stream(cls, stream: BinaryIO, header: 'SenseX1000Base.AcqHeader', seq_num: int, n_sweeps: int):
            # Calculate and read requested number of bytes from stream and create an AcqData object
            data = stream.read(n_sweeps * header.trace_count * header.data_points * header.data_size)
            return SenseX1000Base.AcqData(data, header, seq_num, n_sweeps)

        def __init__(self, data: bytes, header: 'SenseX1000Base.AcqHeader', seq_num: int, n_sweeps: int) -> None:
            # Construct object from binary data, current header and sweep sequence number/number of sweeps
            self.header = header
            self.n_sweeps = n_sweeps
            self.n_traces = header.trace_count
            self.n_points = header.data_points
            self.trace_list = header.trace_list
            self.seq_nums = list(range(seq_num, seq_num + n_sweeps))

            # Calculate directions (alternating sign if ALTERNATING flag is set, otherwise constant sign)
            self.sweep_dir = 1 if header.acq_flags & SenseX1000Base.AcqFlags.DIRECTION else -1
            self.sweep_dirs = [(-self.sweep_dir if seq_num % 2 else self.sweep_dir)
                               if header.acq_flags & SenseX1000Base.AcqFlags.ALTERNATING
                               else self.sweep_dir for seq_num in self.seq_nums]

            # use binary data buffer to construct numpy array and put into correct shape
            self.array = np.reshape(np.frombuffer(data, dtype=header.acq_dtype.info.np),
                                    [n_sweeps, header.trace_count, header.data_points])

    class Acquisition(object):
        """Container class representing an entire acquisition"""
        _header: 'SenseX1000Base.AcqHeader'
        _stream: BinaryIO

        @classmethod
        def from_stream(cls, stream: BinaryIO) -> 'SenseX1000Base.Acquisition':
            """Create acquisition header from the device data stream and instantiate an Acquisition object"""
            header = SenseX1000Base.AcqHeader.from_stream(stream)
            return SenseX1000Base.Acquisition(header=header, stream=stream)

        def __init__(self, header: 'SenseX1000Base.AcqHeader', stream: BinaryIO):
            # Initialize variables required acquisition logic
            self._header = header
            self._stream = stream
            self._sweeps_remaining = header.sweep_count
            self._seq_num = 0

        @property
        def header(self):
            """The header object associated with this acquisition"""
            return self._header

        @property
        def sweeps_remaining(self):
            """The number of sweeps that can still be read from this acquisition"""
            return self._sweeps_remaining

        @property
        def seq_num(self):
            """The sequence number of the acquisition next to be read"""
            return self._seq_num

        def read(self, n_sweeps=-1) -> 'SenseX1000Base.AcqData':
            """Read given number of sweeps (or all sweeps by default) from device"""
            # Determine actual number of sweeps available to be read
            # Create data object from device stream
            # Advance variables
            n = self._sweeps_remaining if n_sweeps < 0 else min(n_sweeps, self._sweeps_remaining)
            data = SenseX1000Base.AcqData.from_stream(self._stream, self._header, self._seq_num, n)
            self._sweeps_remaining -= n
            self._seq_num += n
            return data

        def data(self, n_sweeps=1):
            """Returns a generator object producing an AcqData object with given number of sweeps per iteration"""

            # generator syntax
            while self._sweeps_remaining > 0:
                yield self.read(n_sweeps=n_sweeps)
