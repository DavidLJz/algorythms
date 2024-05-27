from sqlite3 import Connection
from typing import List, Optional
from dataclasses import dataclass

from src.modules.tracks.domain import (
	Track,
	Artist,
	Album,
	Genre,
	Mood,
	TrackPlayHistory,
	GenericRepository,
	Entity
)

@dataclass(eq=True, frozen=True)
class TrackModel:
	title :str
	length :float # In seconds
	album_id: Optional[int] = None
	id: Optional[int] = None
	play_count :Optional[int] = None

	@staticmethod
	def from_entity(track:Track):
		album_id = None if not track.album else track.album.id

		return TrackModel(
			id= track.id,
			title= track.title,
			length= track.length,
			album_id= album_id,
			play_count= track.play_count
		)


class SqliteRepository(GenericRepository[Track]):
	def __init__(self, conn:Connection) -> None:
		self._conn = conn

	def find(self, **kwargs) -> List[Track]:
		_keys = {
			'id': 't.id = ?',
			'title': 't.title = ?',
			'album_id': 't.album_id = ?',
			'like_title': "t.title LIKE CONCAT(?, '%')"
		}

		wherelist = ()
		valuelist = ()

		for _key, where_str in _keys.items():
			if _key not in kwargs:
				continue

			v = kwargs[_key]

			valuelist += (v)
			wherelist += (where_str)

		if len(wherelist) == 0:
			raise ValueError('Not enough arguments')

		sql = '''SELECT 
		t.id, t.title, t.length, t.play_count, t.album_id
		FROM tracks t WHERE
		''' + (' AND '.join(wherelist))

		tracks = []

		with self._conn.cursor() as cursor:
			cursor.execute(sql, valuelist)

			for row in cursor.fetchall():
				tracks.append( 
					Track(
						id= row[0],
						title= row[1],
						length= row[2],
						play_count= row[3],
					) 
				)

		return tracks
	
	def insert(self, entity:Track) -> Track:
		model = TrackModel.from_entity(entity)

		sql = '''INSERT INTO tracks (id, title, length, album_id, play_count) 
		VALUES (?,?,?,?,?)
		'''
		valuelist = (
			model.id, model.title, model.length, model.album_id, model.play_count
		)

		with self._conn.cursor() as cursor:
			cursor.execute(sql, valuelist)

			self._conn.commit()

			_id = cursor.lastrowid

		return Track(**{ 'id':_id, **entity.dump() })
	
	def update(self, entity: Track) -> bool:
		model = TrackModel.from_entity(entity)

		sql = '''UPDATE tracks SET title=?, length=?, album_id=?, play_count=?
		WHERE id=?
		'''

		valuelist = (
			model.title, model.length, model.album_id, model.play_count, model.id
		)

		with self._conn.cursor() as cursor:
			cursor.execute(sql, valuelist)

			self._conn.commit()

			return cursor.rowcount > 0
		
	def up_play_count(self, entity: Track):
		entity.play_count += 1

		if not self.update(entity):
			raise RuntimeError('Error updating')
		
		return entity

	def upsert(self, entity: Track):
		model = TrackModel.from_entity(entity)

		can_update = model.id != None

		if not can_update and model.album_id:
			tracks = self.find(album_id= model.album_id, title= model.title)

			if len(tracks) > 0:
				can_update = True
				entity = tracks[0]

		if can_update:
			if not self.update(entity):
				raise RuntimeError('Error updating')

		return self.insert(entity)

	def delete(self, entity: Track) -> bool:
		model = TrackModel.from_entity(entity)

		sql = '''DELETE FROM tracks SET title=?, length=?, album_id=?, play_count=?
		WHERE id=?
		'''

		valuelist = (
			model.title, model.length, model.album_id, model.play_count, model.id
		)

		with self._conn.cursor() as cursor:
			cursor.execute(sql, valuelist)

			self._conn.commit()

			return cursor.rowcount > 0