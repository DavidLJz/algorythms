from json import dumps
from abc import abstractmethod, ABC
from dataclasses import dataclass, fields, field, asdict
from typing import Any, Optional, List
from datetime import datetime


def dict_to_hashable_tuple(d):
    """
    Recursively converts a dictionary of dictionaries to a tuple that can be hashed.
    
    Args:
        d (dict): The dictionary to be converted.
        
    Returns:
        tuple: A hashable tuple representation of the input dictionary.
    """
    if isinstance(d, dict):
        return tuple((k, dict_to_hashable_tuple(v)) for k, v in sorted(d.items()))
    elif isinstance(d, list):
        return tuple(dict_to_hashable_tuple(item) for item in d)
    else:
        return d


class ValueObject(ABC):
	@abstractmethod
	def get_value(self):
		pass


class StrValue(ValueObject):
	value: str

	@staticmethod
	def from_str(value):
		if isinstance(value, StrValue):
			return value

		return StrValue(value=value)
	
	def get_value(self):
		return self.value

	def __str__(self) -> str:
		return self.value


class AggregateRoot:
	def dump(self):
		d = { k: v.get_value() if isinstance(v, ValueObject) else v for k,v in asdict(self).items() }

		return d
	
	def custom_hash(self):
		return hash(dumps(self.dump(), default=str))


@dataclass(eq=True, frozen=True)
class Genre(StrValue):
	pass


@dataclass(eq=True, frozen=True)
class Mood(StrValue):
	pass


@dataclass(eq=True)
class Artist(AggregateRoot):
	name :str
	aliases :List[str] = field(default_factory= lambda: [])
	genres :List[str|Genre] = field(default_factory= lambda: [])

	def __post_init__(self):
		self.genres = [Genre.from_str(g) for g in self.genres]

	def __hash__(self) -> int:
		return self.custom_hash()



@dataclass(eq=True)
class Album(AggregateRoot):
	name :str
	artists :List[Artist]

	record_label :Optional[str] = None
	genres :List[str|Genre] = field(default_factory= lambda: [])
	moods :List[str|Mood] = field(default_factory= lambda: [])
	release_date :Optional[datetime] = None

	id :Optional[int] = None
	play_count :Optional[int] = None

	def __post_init__(self):
		self.genres = [Genre.from_str(g) for g in self.genres]
		self.moods = [Mood.from_str(g) for g in self.moods]

	def __hash__(self) -> int:
		return self.custom_hash()


@dataclass(eq=True)
class Track(AggregateRoot):
	title :str
	length :float # In seconds
	artists :List[Artist]
	composers :List[Artist] = field(default_factory= lambda: [])

	album :Optional[Album] = None
	genres :List[str|Genre] = field(default_factory= lambda: [])
	moods :List[str|Mood] = field(default_factory= lambda: [])

	id :Optional[int] = None
	play_count :Optional[int] = None

	def __post_init__(self):
		self.genres = [Genre.from_str(g) for g in self.genres]
		self.moods = [Mood.from_str(g) for g in self.moods]

	def __hash__(self) -> int:
		return self.custom_hash()

@dataclass(eq=True)
class TrackPlayHistory(AggregateRoot):
  track_id :int
  played_at :datetime
  id :int = None