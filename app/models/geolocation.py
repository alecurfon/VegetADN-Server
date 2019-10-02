# # coding=utf-8
#
# from . import Base
# from sqlalchemy import Column, String, Integer, ForeignKey
#
# class Geolocation(Base):
#     __tablename__ = 'geolocation'
#
#     geo_id = Column(Integer, primary_key=True)
#     bioentry_id = Column(Integer, ForeignKey("bioentry.bioentry_id"))
#     latitude = Column(Integer)
#     longitude = Column(Integer)
#     biome = Column(String(20))
#     district = Column(String(20))
#     sector = Column(String(20))
#     province = Column(String(20))
#     region = Column(String(20))
#     kingdom = Column(String(20))
#
#
#     def __init__(self, x, y, biome, district, sector, province, region, kingdom):
#         self.id = id
#         self.geo_id = geo_id
#         self.latitude = x
#         self.longitude = y
#         self.biome = biome
#         self.district = district
#         self.sector = sector
#         self.province = province
#         self.region = region
#         self.kingdom = kingdom
#
#     def serialize(self):
#         return {
#             'geo_id':geo_id,
#             'bioentry_id':bioentry_id,
#             'latitude':latitude,
#             'longitude':longitude,
#             'biome':biome,
#             'district':district,
#             'sector':sector,
#             'province':province,
#             'region':region,
#             'kingdom':kingdom
#         }
#
# Base.metadata.create_all(engine)
