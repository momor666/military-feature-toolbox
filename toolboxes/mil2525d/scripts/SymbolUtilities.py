# ----------------------------------------------------------------------------------
# Copyright 2015 Esri
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ----------------------------------------------------------------------------------
# SymbolUtilities.py
# Description: Military Feature Symbol Utilities
# Requirements: ArcGIS Desktop
# ----------------------------------------------------------------------------------

import csv
import os

class SymbolIdCodeDelta(object) :

	def __init__(self) :
		self.version           = '10'
		self.affiliation       = '1'
		self.real_exercise_sim = '0'
		self.symbol_set  = '00'
		self.status      = '0'
		self.hq_tf_fd    = '0'
		self.echelon_mobility = '00'
		self.entity_code = '000000'
		self.modifier1   = '00'
		self.modifier2   = '00' 

	def left_zero_pad(string_in, required_length):
		 return string_in.zfill(required_length)

	def is_valid(self):
		return self.symbol_set != '00'

	# full_code - to set the full code all at once
	@property
	def full_code(self):

		# TODO: 
		# if not full_code_valid :
		populate_code_from_properties()

		return self.__full_code

	@full_code.setter
	def full_code(self, full_code):
		self.__full_code = full_code	
		populate_properties_from_code()

	#####################################################
	# 2525D: A.5.2.1  Set A - First ten digits 

	# version (Digits 1 and 2) 
	@property
	def version(self):
		return self.__version

	@version.setter
	def version(self, version):
		REQUIRED_LENGTH = 2
		if len(version) > REQUIRED_LENGTH :
			return
		self.__version = SymbolIdCodeDelta.left_zero_pad(version, REQUIRED_LENGTH)

	# real_exercise_sim (Digit 3)
	@property
	def real_exercise_sim(self):
		return self.__real_exercise_sim

	@real_exercise_sim.setter
	def real_exercise_sim(self, real_exercise_sim):
		REQUIRED_LENGTH = 1
		if len(real_exercise_sim) > REQUIRED_LENGTH :
			return
		self.__real_exercise_sim = real_exercise_sim

	# affiliation (Digit 4)
	@property
	def affiliation(self):
		return self.__affiliation

	@affiliation.setter
	def affiliation(self, affiliation):
		REQUIRED_LENGTH = 1
		if len(affiliation) > REQUIRED_LENGTH :
			return
		self.__affiliation = affiliation

	# symbol_set (Digits 5 and 6)
	@property
	def symbol_set(self):
		return self.__symbol_set

	@symbol_set.setter
	def symbol_set(self, symbol_set):
		REQUIRED_LENGTH = 2
		if len(symbol_set) > REQUIRED_LENGTH :
			return
		self.__symbol_set = SymbolIdCodeDelta.left_zero_pad(symbol_set, REQUIRED_LENGTH)

	# status (Digit 7)
	@property
	def status(self):
		return self.__status

	@status.setter
	def status(self, status):
		REQUIRED_LENGTH = 1
		if len(status) > REQUIRED_LENGTH :
			return
		self.__status = status

	# hq_tf_fd (Digit 8)
	@property
	def hq_tf_fd(self):
		return self.__hq_tf_fd

	@hq_tf_fd.setter
	def hq_tf_fd(self, hq_tf_fd):
		REQUIRED_LENGTH = 1
		if len(hq_tf_fd) > REQUIRED_LENGTH :
			return
		self.__hq_tf_fd = hq_tf_fd

	# echelon_mobility (Digits 9 and 10)
	@property
	def echelon_mobility(self):
		return self.__echelon_mobility

	@echelon_mobility.setter
	def echelon_mobility(self, echelon_mobility):
		REQUIRED_LENGTH = 2
		if len(echelon_mobility) > REQUIRED_LENGTH :
			return
		self.__echelon_mobility = SymbolIdCodeDelta.left_zero_pad(echelon_mobility, REQUIRED_LENGTH)

	#####################################################
	# 2525D: A.5.2.2  Set B - Second ten digits

	# (full) entity_code (Digits 11-16) 
	@property
	def entity_code(self):
		return self.__entity_code

	@entity_code.setter
	def entity_code(self, entity_code):
		REQUIRED_LENGTH = 6
		if len(entity_code) > REQUIRED_LENGTH :
			return
		self.__entity_code = SymbolIdCodeDelta.left_zero_pad(entity_code, REQUIRED_LENGTH)

	# modifier1 (Digits 17 and 18)
	@property
	def modifier1(self):
		return self.__modifier1

	@modifier1.setter
	def modifier1(self, modifier1):
		REQUIRED_LENGTH = 2
		if len(modifier1) > REQUIRED_LENGTH :
			return
		self.__modifier1 = SymbolIdCodeDelta.left_zero_pad(modifier1, REQUIRED_LENGTH)

	# modifier (Digits 19 and 20)
	@property
	def modifier2(self):
		return self.__modifier2

	@modifier2.setter
	def modifier2(self, modifier2):
		REQUIRED_LENGTH = 2
		if len(modifier2) > REQUIRED_LENGTH :
			return
		self.__modifier2 = SymbolIdCodeDelta.left_zero_pad(modifier2, REQUIRED_LENGTH)

	#####################################################

	def populate_code_from_properties(self):
		# TODO
		pass

	def populate_properties_from_code(self):
		# TODO
		pass

	def human_readable_code(self):
		string_builder = "SS:"   + self.symbol_set
		string_builder+= ":E:"   + self.entity_code
		string_builder+= ":M1:"  + self.modifier1
		string_builder+= ":M2:"  + self.modifier2
		string_builder+= ":A:"   + self.affiliation
		string_builder+= ":RES:" + self.real_exercise_sim

		# optional ones
		if not (self.status is None or self.status == '0') :
			string_builder+= ":ST:" + self.status
		if not (self.echelon_mobility is None or self.echelon_mobility == '00') :
			string_builder+= ":EM:" + self.echelon_mobility
		if not (self.hq_tf_fd is None or self.hq_tf_fd == '0') :
			string_builder+= ":HTD:" + self.hq_tf_fd

		return string_builder


###############################################################################

class SymbolLookup(object) :

	def __init__(self) :

		self.idDict2525CtoD = {}
		self.initialize()

	def initialized(self) : 
		return len(self.idDict2525CtoD) > 0

	def initialize(self) :

		if self.initialized() :
			return True

		currentPath = os.path.dirname(__file__)
		dataPath = os.path.normpath(os.path.join(currentPath, r"../tooldata"))
		inputFile  = os.path.normpath(os.path.join(dataPath, r"LegacyMappingTableCtoD.csv"))

		print("Initializing using source data: " + inputFile)

		# Open Input File & load into dict (if possible)
		try :            
			with open(inputFile, "r") as f_in :

				reader = csv.reader(f_in, delimiter=',')

				next(reader, None) # skip header row

				# Expected Format:
				#  {2525Charlie1stTen : 2525Charlie1stTen,2525Charlie,2525DeltaSymbolSet,
				#     2525DeltaEntity,2525DeltaMod1,2525DeltaMod2,2525DeltaName,2525DeltaMod1Name,
				#     2525DeltaMod2Name,DeltaToCharlie,Remarks}

				self.idDict2525CtoD = {row[0]:row for row in reader}

		except Exception as openEx :            
			print('Could not open Output File for reading: ' + str(inputFile))
			return

		return self.initialized()

	# If debug needed
	# for key in idDict2525CtoD :
	#	print(key)
	

	def getDeltaCodeFromCharlie(self, charlieCode) : 

		symbolId = SymbolIdCodeDelta()

		MINIMUM_CODE_LENGTH = 10

		if (not self.initialized()) or (charlieCode is None) or (len(charlieCode) < MINIMUM_CODE_LENGTH) :
			return symbolId 

		symbolSetString = '98'
		entityString    = '100000'
		mod1String      = '00'
		mod2String      = '00'

		isWeather = (charlieCode[0] == 'W')

		replaceAffilChar  = '*'
		replaceStatusChar = 'P'
		if (isWeather) :
			replaceAffilChar  = charlieCode[1]
			replaceStatusChar = charlieCode[3]

		lookupCharlieCode = charlieCode[0]
		lookupCharlieCode+= replaceAffilChar
		lookupCharlieCode+= charlieCode[2]
		lookupCharlieCode+= replaceStatusChar
		lookupCharlieCode+= charlieCode[4:10]

		print("Using Charlie Lookup: " + lookupCharlieCode)

		try : 
			if not (lookupCharlieCode in self.idDict2525CtoD) :
				# some keys only have an "F" version
				alternateLookupKey = lookupCharlieCode[0] + 'F' + lookupCharlieCode[2:10]
				if not (alternateLookupKey in self.idDict2525CtoD) :
					print("Could not find key: " + lookupCharlieCode)
					return symbolId
				else :
					lookupCharlieCode = alternateLookupKey

			row2525d = self.idDict2525CtoD[lookupCharlieCode]

			symbolSetString = row2525d[2]
			entityString    = row2525d[3]
			mod1String      = row2525d[4]
			mod2String      = row2525d[5]

			remarks = row2525d[10]

			if remarks == 'Retired' :
				print("Retired Symbol" + lookupCharlieCode)

		except : 
			print("Crash with key: " + lookupCharlieCode)

		symbolId.symbol_set  = symbolSetString
		symbolId.entity_code = entityString
		symbolId.modifier1   = mod1String
		symbolId.modifier2   = mod2String

		# now we have the base symbol, but the remaining attributes are a little messier to map 
		# TODO: Affiliation, Planning/Status, HQ_TF_FD, Echelon

		return symbolId 