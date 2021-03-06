# encoding: utf-8

from AppKit import *
from Foundation import *

import time, math, sys, os


__all__ = ["Glyphs", "GetFile", "GSMOVE", "GSLINE", "GSCURVE", "GSOFFCURVE", "GSSHARP", "GSSMOOTH", "TOPGHOST", "STEM", "BOTTOMGHOST", "TTANCHOR", "TTSTEM", "TTALIGN", "TTINTERPOLATE", "TTDIAGONAL", "CORNER", "CAP", "TTDONTROUND", "TTROUND", "TTROUNDUP", "TTROUNDDOWN", "TRIPLE", "divideCurve", "distance", "addPoints", "subtractPoints", "GetFolder", "GetSaveFile", "GetOpenFile", "Message", "newTab"]


class Proxy(object):
	def __init__(self, owner):
		self._owner = owner
	def __repr__(self):
		"""Return list-lookalike of representation string of objects"""
		strings = []
		for currItem in self:
			strings.append("%s" % (currItem))
		return "(%s)" % (', '.join(strings))
	def __len__(self):
		Values = self.values()
		if Values is not None:
			return len(self.values())
		return 0
	def __iter__(self):
		Values = self.values()
		if Values is not None:
			for element in Values:
				yield element
	def index(self, Value):
		return self.values().index(Value)


##################################################################################
#
#
#
#           GSApplication
#
#
#
##################################################################################


Glyphs = NSApplication.sharedApplication()


'''
:mod:`GSApplication`
===============================================================================

Some usefull methods on application level. The global "Glyphs" object give access to them. e.g. Glyphs.font
	
.. class:: GSApplication

**Properties**

.. autosummary::
	fonts
	font
	defaults
	boolDefaults
	intDefaults
	
**Functions**

.. autosummary::

	open()
	showMacroWindow()
	clearLog()
	showGlyphInfoPanelWithSearchString()
	
----------
Properties
----------
'''
GSApplication.currentDocument = property(lambda self: NSDocumentController.sharedDocumentController().currentDocument())

GSApplication.documents = property(lambda self: AppDocumentProxy(self))

def Glyphs__repr__(self):
	return '<Glyphs.app>'
GSApplication.__repr__ = Glyphs__repr__;

def currentFont():
	doc = NSDocumentController.sharedDocumentController().currentDocument()
	if (doc):
		return doc.font

# by Yanone
GSApplication.font = property(lambda self: currentFont())

'''.. attribute:: font
	
	:return: The active :class:`Font <GSFont>` object or None.
	:rtype: :class:`GSFont <GSFont>`'''

# by Yanone
def AllFonts():
	fonts = []
	for d in NSDocumentController.sharedDocumentController().documents():
		fonts.append(d.font)
	return fonts
GSApplication.fonts = property(lambda self: AllFonts())

'''.. attribute:: fonts
	
	:return: All open :class:`Fonts <GSFont>`.
	:rtype: list'''

class DefaultsProxy(Proxy):
	def __getitem__(self, Key):
		return NSUserDefaults.standardUserDefaults().objectForKey_(Key)
	def __setitem__(self, Key, Value):
		NSUserDefaults.standardUserDefaults().setObject_forKey_(Value, Key)
	def __repr__(self):
		return "<Userdefaults>"

GSApplication.defaults = property(lambda self: DefaultsProxy(self))

'''.. attribute:: defaults
	
	A dict like object. You can get and set key value pairs.
	
	Please be careful with your keys. Use a prefix that uses the reverse domain name. e.g. "com.MyName.foo.bar".
	
	use it like this:
	
	.. code-block:: python
	
		Value = Glyphs.defaults["com.MyName.foo.bar"]
		Glyphs.defaults["com.MyName.foo.bar"] = NewValue
	
	'''


class BoolDefaultsProxy(DefaultsProxy):
	def __getitem__(self, Key):
		return NSUserDefaults.standardUserDefaults().boolForKey_(Key)
	def __setitem__(self, Key, Value):
		NSUserDefaults.standardUserDefaults().setBool_forKey_(Value, Key)

GSApplication.boolDefaults = property(lambda self: BoolDefaultsProxy(self))

'''.. attribute:: boolDefaults
	
	A dict like object. Same as Glyphs.defaults only that value is a bool.
	
	Please be careful with your keys. Use a prefix that uses the reverse domain name. e.g. "com.MyName.foo.bar".
	'''

class IntDefaultsProxy(DefaultsProxy):
	def __getitem__(self, Key):
		return NSUserDefaults.standardUserDefaults().integerForKey_(Key)
	def __setitem__(self, Key, Value):
		NSUserDefaults.standardUserDefaults().setInteger_forKey_(Value, Key)

GSApplication.intDefaults = property(lambda self: IntDefaultsProxy(self))

'''.. attribute:: intDefaults
	
	A dict like object. Same as Glyphs.defaults only that value is a int.
	
	Please be careful with your keys. Use a prefix that uses the reverse domain name. e.g. "com.MyName.foo.bar".
	
	'''




'''
---------
Functions
---------
'''

def OpenFont(self, Path, showInterface=True ):
	URL = NSURL.fileURLWithPath_(Path)
	Doc = NSDocumentController.sharedDocumentController().openDocumentWithContentsOfURL_display_error_(URL, showInterface, None)
	if Doc is not None:
		return Doc.font
	return None
	
GSApplication.open = OpenFont

'''.. function:: open(Path)
	
	Opens a document
	
	:param Path: The path where the document is located.
	:type Path: str
	:return: The opened document object or None.
	:rtype: :class:`Font <GSFont>`'''

def __ShowMacroWindow(self):
	GSApplication.delegate(self).showMacroWindow()

GSApplication.showMacroWindow = __ShowMacroWindow

'''.. function:: showMacroWindow
	
	Opens the macro window

'''

def __ClearLog(self):
	GSApplication.delegate(self).clearConsole()

GSApplication.clearLog = __ClearLog

'''.. function:: clearLog
	
	Deletes the content of the console in the macro window
	
'''


def __showGlyphInfoPanelWithSearchString__(self, String):
	GSApplication.delegate(self).showGlyphInfoPanelWithSearchString_(String)

GSApplication.showGlyphInfoPanelWithSearchString = __showGlyphInfoPanelWithSearchString__

'''.. function:: showGlyphInfoPanelWithSearchString(String)
	
	Shows the Glyph Info window with a preset search string
	
	:param String: The search term
	
	'''



GSMOVE = 17
GSLINE = 1
GSCURVE = 35
GSOFFCURVE = 65
GSSHARP = 0
GSSMOOTH = 100

TOPGHOST = -1
STEM = 0
BOTTOMGHOST = 1
TTANCHOR = 2
TTSTEM = 3
TTALIGN = 4
TTINTERPOLATE = 5
TTDIAGONAL = 6
CORNER = 16
CAP = 17

TTDONTROUND = 4,
TTROUND = 0,
TTROUNDUP = 1,
TTROUNDDOWN = 2,
TRIPLE = 128,

# Reverse lookup for __repr__
nodeConstants = {
	17: 'GSMOVE',
	1: 'GSLINE',
	35: 'GSCURVE',
	65: 'GSOFFCURVE',
	0: 'GSSHARP',
	100: 'GSSMOOTH',
}
hintConstants = {
	-1: 'TopGhost',
	0: 'Stem',
	1: 'BottomGhost',
	2: 'TTAnchor',
	3: 'TTStem',
	4: 'TTAlign',
	5: 'TTInterpolate',
	6: 'TTDiagonal',
	16: 'Corner',
	17: 'Cap',
}



GSElement.x = property(lambda self: self.pyobjc_instanceMethods.position().x,
	lambda self, value: self.setPosition_(NSMakePoint(value, self.y)))

GSElement.y = property(lambda self: self.pyobjc_instanceMethods.position().y,
	lambda self, value: self.setPosition_(NSMakePoint(self.x, value)))


class AppDocumentProxy (Proxy):
	"""The list of documents."""
	#NSDocumentController.sharedDocumentController().documents()
	def __getitem__(self, Key):
		if type(Key) is int:
			if Key < 0:
				Key = self.__len__() + Key
			return NSDocumentController.sharedDocumentController().documents().objectAtIndex_(Key)
		else:
			raise(KeyError)
	def __len____(self):
		return NSDocumentController.sharedDocumentController().documents().count()
	def values(self):
		return NSDocumentController.sharedDocumentController().documents()


GSDocument.font = property(lambda self: self.valueForKey_("font"),
						   lambda self, value: self.setFont_(value))

#	''.. attribute:: font
#		The active :class:`Font <GSFont>`.
#		:type: list''





class FontGlyphsProxy (Proxy):
	"""The list of glyphs. You can access it with the index or the glyph name.
	Usage: 
		Font.glyphs[index]
		Font.glyphs[name]
		for glyph in Font.glyphs:
		...
	"""
	def __getitem__(self, Key):
		if type(Key) is int:
			if Key < 0:
				Key = self.__len__() + Key
			return self._owner.glyphAtIndex_(Key)
		else:
			return self._owner.glyphForName_(Key)
	def __setitem__(self, Key, Glyph):
		if type(Key) is int:
			self._owner.removeGlyph_( self._owner.glyphAtIndex_(Key) )
			self._owner.addGlyph_(Glyph)
		else:
			self._owner.removeGlyph_( self._owner.glyphForName_(Key) )
			self._owner.addGlyph_(Glyph)
	def __delitem__(self, Key):
		if type(Key) is int:
			self._owner.removeGlyph_( self._owner.glyphAtIndex_(Key) )
		else:
			self._owner.removeGlyph_( self._owner.glyphForName_(Key) )
	def __contains__(self, item):
		return self._owner.indexOfGlyph_(item) < NSNotFound #indexOfGlyph_ returns NSNotFound which is some very big number
	def keys(self):
		return self._owner.pyobjc_instanceMethods.glyphs().valueForKeyPath_("@unionOfObjects.name")
	def values(self):
		return self._owner.pyobjc_instanceMethods.glyphs()
	def items(self):
		Items = []
		for Value in self._owner.pyobjc_instanceMethods.glyphs():
			Key = Value.name
			Items.append((Key, Value))
		return Items
	def has_key(self, Key):
		return self._owner.glyphForName_(Key) != None
	def append(self, Glyph):
		self._owner.addGlyph_(Glyph)
	def __len__(self):
		return self._owner.count()


class FontFontMasterProxy (Proxy):
	def __getitem__(self, Key):
		if type(Key) is int:
			if Key < 0:
				Key = self.__len__() + Key
			return self._owner.fontMasterAtIndex_(Key)
		elif type(Key) is str or type(Key) is unicode or type(Key) is objc.pyobjc_unicode:
			return self._owner.fontMasterForId_(Key)
		else:
			raise(KeyError)
	def __setitem__(self, Key, FontMaster):
		if type(Key) is int:
			self._owner.replaceFontMasterAtIndex_withFontMaster_(Key, FontMaster)
		elif type(Key) is str or type(Key) is unicode or type(Key) is objc.pyobjc_unicode:
			OldFontMaster = self._owner.fontMasterForId_(Key)
			self._owner.removeFontMaster_(OldFontMaster)
			return self._owner.addFontMaster_(FontMaster)
	def __delitem__(self, Key):
		if type(Key) is int:
			return self._owner.removeFontMasterAtIndex_(Key)
		else:
			OldFontMaster = self._owner.fontMasterForId_(Key)
			return self._owner.removeFontMaster_(OldFontMaster)
	def __iter__(self):
		for index in range(self._owner.countOfFontMasters()):
			yield self._owner.fontMasterAtIndex_(index)
	def __len__(self):
		return self._owner.countOfFontMasters()
	def values(self):
		return self._owner.pyobjc_instanceMethods.fontMasters()
	


class FontInstancesProxy (Proxy):
	def __getitem__(self, Key):
		if type(Key) is int:
			if Key < 0:
				Key = self.__len__() + Key
			return self._owner.instanceAtIndex_(Key)
		else:
			raise(KeyError)
	def __setitem__(self, Key, Class):
		if type(Key) is int:
			self._owner.replaceObjectInInstancesAtIndex_withObject_(Key, Class)
	def __delitem__(self, Key):
		if type(Key) is int:
			return self._owner.removeObjectFromInstancesAtIndex_(Key)
	def __iter__(self):
		for index in range(self._owner.countOfInstances()):
			yield self._owner.instanceAtIndex_(index)
	def append(self, Instance):
		self._owner.addInstance_(Instance)
	def __len__(self):
		return self._owner.countOfInstances()
	def values(self):
		return self._owner.pyobjc_instanceMethods.instances()
	

class CustomParametersProxy(Proxy):
	def __getitem__(self, Key):
		if type(Key) is int:
			return self._owner.objectInCustomParametersAtIndex_(Key)
		else:
			return self._owner.customValueForKey_(Key)
	def __setitem__(self, Key, Parameter):
		if type(Key) is int:
			Value = self._owner.objectInCustomParametersAtIndex_(Key)
			if Value is not None:
				Value.setValue_(Parameter)
		else:
			self._owner.setCustomParameter_forKey_(Parameter, Key)
	def __delitem__(self, Key):
		if type(Key) is int:
			self._owner.removeObjectFromCustomParametersAtIndex_(Key)
		else:
			self._owner.removeObjectFromCustomParametersForKey_(Key)
	def __iter__(self):
		for index in range(self._owner.countOfCustomParameters()):
			yield self._owner.objectInCustomParametersAtIndex_(index)
	def append(self, Parameter):
		self._owner.addCustomParameter_(Parameter)
	def __len__(self):
		return self._owner.countOfCustomParameters()
	def values(self):
		return self._owner.pyobjc_instanceMethods.customParameters()
	

class FontClassesProxy (Proxy):
	def __getitem__(self, Key):
		if type(Key) is int:
			if Key < 0:
				Key = self.__len__() + Key
			return self._owner.objectInClassesAtIndex_(Key)
		elif type(Key) is str or type(Key) is unicode or type(Key) is objc.pyobjc_unicode:
			if len(Key) > 0:
				return self._owner.classForTag_(Key)
		raise(KeyError)
	def __setitem__(self, Key, Class):
		if type(Key) is int:
			self._owner.replaceObjectInClassesAtIndex_withObject_(Key, Class)
	def __delitem__(self, Key):
		if type(Key) is int:
			return self._owner.removeObjectFromClassesAtIndex_(Key)
		elif type(Key) is str or type(Key) is unicode or type(Key) is objc.pyobjc_unicode:
			Class = self._owner.classForTag_(Key)
			if Class is not None:
				return self._owner.removeClass_(Class)
	def __iter__(self):
		for index in range(self._owner.countOfClasses()):
			yield self._owner.objectInClassesAtIndex_(index)
	def append(self, Class):
		 # print "append Class", Class
		self._owner.addClass_(Class)
	def __len__(self):
		return self._owner.countOfClasses()
	def values(self):
		return self._owner.pyobjc_instanceMethods.classes()
	

class FontFeaturesProxy (Proxy):
	def __getitem__(self, Key):
		if type(Key) is int:
			if Key < 0:
				Key = self.__len__() + Key
			return self._owner.featureAtIndex_(Key)
		if type(Key) is str or type(Key) is unicode or type(Key) is objc.pyobjc_unicode:
			return self._owner.featureForTag_(Key)
		else:
			raise(KeyError)
	def __setitem__(self, Key, Feature):
		if type(Key) is int:
			self._owner.replaceFeatureAtIndex_withFeature_(Key, Feature)
	def __delitem__(self, Key):
		if type(Key) is int:
			return self._owner.removeFeatureAtIndex_(Key)
		else:
			raise(KeyError)
	def __iter__(self):
		for index in range(self._owner.countOfFeatures()):
			yield self._owner.featureAtIndex_(index)
	def append(self, Feature):
		#print "append", Node
		self._owner.addFeature_(Feature)

	def __len__(self):
		return self._owner.countOfFeatures()
	def text(self):
		LineList = []
		for Feature in self._owner.pyobjc_instanceMethods.features():
			LineList.append("feature ")
			LineList.append(Feature.name)
			LineList.append(" {\n")
			LineList.append("    "+Feature.code)
			LineList.append("\n} ")
			LineList.append(Feature.name)
			LineList.append(" ;\n")
		return "".join(LineList)
	def values(self):
		return self._owner.pyobjc_instanceMethods.features()
	


class FontFeaturePrefixesProxy (Proxy):
	def __getitem__(self, Key):
		if type(Key) is int:
			if Key < 0:
				Key = self.__len__() + Key
			return self._owner.objectInFeaturePrefixesAtIndex_(Key)
		if type(Key) is str or type(Key) is unicode or type(Key) is objc.pyobjc_unicode:
			return self._owner.featurePrefixForTag_(Key)
		else:
			raise(KeyError)
	def __setitem__(self, Key, Feature):
		if type(Key) is int:
			self._owner.replaceObjectInFeaturePrefixesAtIndex__withObject_(Key, Feature)
	def __delitem__(self, Key):
		if type(Key) is int:
			return self._owner.removeObjectFromFeaturePrefixesAtIndex_(Key)
		else:
			raise(KeyError)
	def append(self, Feature):
		#print "append", Node
		self._owner.addFeaturePrefix_(Feature)
	def text(self):
		LineList = []
		for Prefixe in self._owner.pyobjc_instanceMethods.featurePrefixes():
			LineList.append("# "+Prefixe.name)
			LineList.append(Prefixe.code)
		return "".join(LineList)
	def values(self):
		return self._owner.pyobjc_instanceMethods.featurePrefixes()

class LayersIterator:
	def __init__(self, owner):
		self.curInd = 0
		self._owner = owner
	def __iter__(self):
		return self
	def next(self):
		if self._owner.parent:
			if self.curInd >= self._owner.countOfLayers():
				raise StopIteration
			if self.curInd < self._owner.parent.countOfFontMasters():
				FontMaster = self._owner.parent.fontMasterAtIndex_(self.curInd)
				Item = self._owner.layerForKey_(FontMaster.id)
			else:
				ExtraLayerIndex = self.curInd - self._owner.parent.countOfFontMasters()
				Index = 0
				ExtraLayer = None
				while ExtraLayerIndex >= 0:
					ExtraLayer = self._owner.pyobjc_instanceMethods.layers().objectAtIndex_(Index)
					if ExtraLayer.layerId != ExtraLayer.associatedMasterId:
						ExtraLayerIndex = ExtraLayerIndex - 1
					Index = Index + 1
				Item = ExtraLayer
			self.curInd += 1
			return Item
		else:
			if self.curInd >= self._owner.countOfLayers():
				raise StopIteration
			Item = self._owner.pyobjc_instanceMethods.layers().objectAtIndex_(self.curInd)
			self.curInd += 1
			return Item
		return None

class GlyphLayerProxy (Proxy):
	def __getitem__(self, Key):
			if type(Key) is int:
				if Key < 0:
					Key = self.__len__() + Key
				if self._owner.parent:
					if Key < self._owner.parent.countOfFontMasters():
						FontMaster = self._owner.parent.fontMasterAtIndex_(Key)
						return self._owner.layerForKey_(FontMaster.id)
					else:
						ExtraLayerIndex = Key - len(self._owner.parent.masters)
						Index = 0
						ExtraLayer = None
						while ExtraLayerIndex >= 0:
							ExtraLayer = self._owner.pyobjc_instanceMethods.layers().objectAtIndex_(Index)
							if ExtraLayer.layerId != ExtraLayer.associatedMasterId:
								ExtraLayerIndex = ExtraLayerIndex - 1
							Index = Index + 1
						return ExtraLayer
				else:
					return self._owner.pyobjc_instanceMethods.layers().objectAtIndex_(Key)
			else:
				return self._owner.layerForKey_(Key)
	def __setitem__(self, Key, Layer):
		if type(Key) is int and self._owner.parent:
			FontMaster = self._owner.parent.fontMasterAtIndex_(Key)
			return self._owner.setLayer_forKey_(Layer, FontMaster.id)
		else:
			return self._owner.setLayer_forKey_(Layer, Key)
	def __delitem__(self, Key):
		if type(Key) is int and self._owner.parent:
			Layer = self.__getitem__(Key)
			return self._owner.removeLayerForKey_(Layer.layerId)
		else:
			return self._owner.removeLayerForKey_(Key)
	def __iter__(self):
		return LayersIterator(self._owner)
	def __len__(self):
		return self._owner.countOfLayers()
	def values(self):
		return self._owner.pyobjc_instanceMethods.layers().allValues()

class LayerComponentsProxy (Proxy):
	def __getitem__(self, i):
		return self._owner.componentAtIndex_(i)
	def __setitem__(self, i, Component):
		self._owner.setComponent_atIndex_(Component, i)
	def __delitem__(self, i):
		self._owner.removeComponentAtIndex_(i)
	def append(self, Component):
		self._owner.addComponent_(Component)
	def values(self):
		return self._owner.pyobjc_instanceMethods.components()

class LayerGuideLinesProxy (Proxy):
	def __getitem__(self, i):
		return self._owner.guideLineAtIndex_(i)
	def __setitem__(self, i, Component):
		self._owner.setGuideLine_atIndex_(Component, i)
	def __delitem__(self, i):
		self._owner.removeGuideLineAtIndex_(i)
	def append(self, GuideLine):
		self._owner.addGuideLine_(GuideLine)
	def values(self):
		return self._owner.pyobjc_instanceMethods.guideLines()

class LayerHintsProxy (Proxy):
	def __getitem__(self, i):
		return self._owner.hintAtIndex_(i)
	def __setitem__(self, i, Component):
		self._owner.setHint_atIndex_(Component, i)
	def __delitem__(self, i):
		self._owner.removeObjectFromHintsAtIndex_(i)
	def append(self, GuideLine):
		self._owner.addHint_(GuideLine)
	def values(self):
		return self._owner.pyobjc_instanceMethods.hints()
	

class LayerAnchorsProxy (Proxy):
	"""layer.anchors is a dict!!!"""
	def __getitem__(self, Key):
		if type(Key) is str or type(Key) is unicode or type(Key) is objc.pyobjc_unicode:
			return self._owner.anchorForName_(Key)
		else:
			raise KeyError
			return self._owner.pyobjc_instanceMethods.anchors().objectAtIndex_(Key)
	def __setitem__(self, Key, Anchor):
		if type(Key) is str or type(Key) is unicode or type(Key) is objc.pyobjc_unicode:
			Anchor.setName_(Key)
			self._owner.addAnchor_(Anchor)
		else:
			raise TypeError
	def __delitem__(self, Key):
		print "__del anchor", type(Key)
		if type(Key) is str or type(Key) is unicode or type(Key) is objc.pyobjc_unicode:
			self._owner.removeAnchorWithName_(Key)
		else:
			raise TypeError
	def items(self):
		Items = []
		for key in self.keys():
			Value = self._owner.anchorForName_(Key)
			Items.append((Key, Value))
		return Items
	
	def values(self):
		if self._owner.pyobjc_instanceMethods.anchors() is not None:
			return self._owner.pyobjc_instanceMethods.anchors().allValues()
		else:
			return [];
	
	def keys(self):
		if self._owner.pyobjc_instanceMethods.anchors() is not None:
			return self._owner.pyobjc_instanceMethods.anchors().allKeys()
		else:
			return []
	def __len__(self):
		#print "count"
		return self._owner.anchorCount()



class LayerPathsProxy (Proxy):
	def __getitem__(self, Key):
		if Key < 0:
			Key = self._owner.pathCount() + Key
		return self._owner.pathAtIndex_(Key)
	def __setitem__(self, i, Path):
		self._owner.setPath_atIndex_(Path, i)
	def __delitem__(self, i):
		self._owner.removePathAtIndex_(i)
	def append(self, Path):
		self._owner.addPath_(Path)
	def values(self):
		return self._owner.pyobjc_instanceMethods.paths()




class PathNodesProxy (Proxy):
	def __getitem__(self, i):
		#print "__getitem__", i
		return self._owner.nodeAtIndex_(i)
	def __setitem__(self, i, Node):
		#print "__setitem__", i, Node
		self._owner.setNode_atIndex_(Node, i)
	def __delitem__(self, i):
		#print "__delitem__", i
		self._owner.removeNodeAtIndex_(i)
	def append(self, Node):
		#print "append", Node
		self._owner.addNode_(Node)
	def values(self):
		return self._owner.pyobjc_instanceMethods.nodes()





##################################################################################
#
#
#
#           GSFont
#
#
#
##################################################################################

		
'''
:mod:`GSFont`
===============================================================================

Implementation of the font object. This object is host to the :class:`Masters <GSFontMaster>` used for interpolation. Even when no interpolation is involved, for the sake of object model consistency there will still be one master and one instance representing a single font.

Also, the :class:`Glyphs <GSGlyph>` are attached to the Font object right here, not one level down to the masters. The different master's glyphs are available as :class:`Layers <GSLayer>` attached to the :class:`Glyph <GSGlyph>` objects which are attached here.

.. class:: GSFont

**Properties**

.. autosummary::

	masters
	instances
	glyphs
	classes
	features
	featurePrefixes
	copyright
	designer
	designerURL
	manufacturer
	manufacturerURL
	versionMajor
	versionMinor
	date
	familyName
	upm
	note
	kerning
	userData
	gridLength
	disablesNiceNames
	customParameters
	filepath
	selectedFontMaster
	selectedLayers
	currentText

**Functions**

.. autosummary::
	
	disableUpdateInterface()
	enableUpdateInterface()
	kerningForPair()
	setKerningForPair()
	removeKerningForPair()

----------
Properties
----------

'''


def Font__new__(typ, *args, **kwargs):
	if len(args) > 0 and (type(args[0]) == type(str) or type(args[0]) == type(unicode)):
		path = args[0]
		URL = NSURL.fileURLWithPath_(path)
		typeName = NSWorksSpace.sharedWorkspace().typeOfFile_error_(path, None)
		Doc = GSDocument.alloc().initWithContentsOfURL_ofType_error_(URL, typeName, None)
		if Doc is not None:
			return Doc.font()
		raise("Unable to open font")
	else:
		return GSFont.alloc().init()
GSFont.__new__ = Font__new__

def Font__init__(self, path=None):
	pass

GSFont.__init__ = Font__init__

def Font__repr__(self):
	return "<GSFont \"%s\" v%s.%s with %s masters and %s instances>" % (self.familyName, self.versionMajor, self.versionMinor, len(self.masters), len(self.instances))
GSFont.__repr__ = Font__repr__

def Font__save__(self, path=None):
	print "__save__", self.parent
	if self.parent is not None:
		if path is None:
			self.parent.saveDocument_(None)
		else:
			URL = NSURL.fileURLWithPath_(path)
			self.parent.writeSafelyToURL_ofType_forSaveOperation_error_(URL, self.parent.typeName, 1, objc.nil)
	elif path is not None:
		Doc = GSDocument.alloc().init()
		Doc.font = self
		URL = NSURL.fileURLWithPath_(path)
		if path.endswith('.glyphs'):
			typeName = "com.schriftgestaltung.glyphs"
		elif path.endswith('.ufo'):
			typeName = "org.unifiedfontobject.ufo"
		print "writeSafelyToURL", Doc.writeSafelyToURL_ofType_forSaveOperation_error_(URL, typeName, 1, objc.nil)
	else:
		raise("Now path set")
		
GSFont.save = Font__save__

def Font__close__(self, ignoreChanges=True):
	if self.parent:
		if ignoreChanges:
			self.parent.close()
		else:
			self.parent.canCloseDocumentWithDelegate_shouldCloseSelector_contextInfo_(None, None, None)
GSFont.close = Font__close__

GSFont.parent = property(lambda self: self.valueForKey_("parent"))

GSFont.masters = property(lambda self: FontFontMasterProxy(self),
						  lambda self, value: self.setFontMasters_(NSMutableArray.arrayWithArray_(value)))
'''.. attribute:: masters
	Collection of :class:`GSFontMaster <GSFontMaster>`.
	:type: list'''

GSFont.instances = property(lambda self: FontInstancesProxy(self),
							lambda self, value: self.setInstances_(NSMutableArray.arrayWithArray_(value)))
'''.. attribute:: instances
	Collection of :class:`GSInstance <GSInstance>`.
	:type: list'''

GSFont.glyphs = property(lambda self: FontGlyphsProxy(self),
						 lambda self, value: self.setGlyphs_(NSMutableArray.arrayWithArray_(value)))
'''.. attribute:: glyphs
	Collection of :class:`GSGlyph <GSGlyph>`. Returns a list, but you may also call glyphs using index or glyph name as key.
	.. code-block:: python
		print font.glyphs['A']
		<GSGlyph "A" with 4 layers>
	.. code-block:: python
		print font.glyphs[20]
		<GSGlyph "Aacute" with 2 layers>
	:type: list, dict'''
GSFont.classes = property(lambda self: FontClassesProxy(self),
						  lambda self, value: self.setClasses_(NSMutableArray.arrayWithArray_(value)))
'''.. attribute:: classes
	Collection of :class:`GSClass <GSClass>` objects, representing OpenType glyph classes.
	:type: list'''
GSFont.features = property(lambda self: FontFeaturesProxy(self),
						   lambda self, value: self.setFeatures_(NSMutableArray.arrayWithArray_(value)))
'''.. attribute:: features
	Collection of :class:`GSFeature <GSFeature>` objects, representing OpenType features.
	:type: list'''

GSFont.featurePrefixes = property(lambda self: FontFeaturePrefixesProxy(self),
								  lambda self, value: self.setFeaturePrefixes_(NSMutableArray.arrayWithArray_(value)))
'''.. attribute:: featurePrefixes
	Collection of :class:`GSFeaturePrefix <GSFeaturePrefix>` objects, containing stuff that needs to be outside of the OpenType features.
	:type: list'''

GSFont.copyright = property(lambda self: self.valueForKey_("copyright"), lambda self, value: self.setValue_forKey_(value, "copyright"))
'''.. attribute:: copyright
	:type: unicode'''
GSFont.designer = property(lambda self: self.valueForKey_("designer"), lambda self, value: self.setValue_forKey_(value, "designer"))
'''.. attribute:: designer
	:type: unicode'''
GSFont.designerURL = property(lambda self: self.valueForKey_("designerURL"), lambda self, value: self.setValue_forKey_(value, "designerURL"))
'''.. attribute:: designerURL
	:type: unicode'''
GSFont.manufacturer = property(lambda self: self.valueForKey_("manufacturer"), lambda self, value: self.setValue_forKey_(value, "manufacturer"))
'''.. attribute:: manufacturer
	:type: unicode'''
GSFont.manufacturerURL = property(lambda self: self.valueForKey_("manufacturerURL"), lambda self, value: self.setValue_forKey_(value, "manufacturerURL"))
'''.. attribute:: manufacturerURL
	:type: unicode'''
GSFont.versionMajor = property(lambda self: self.valueForKey_("versionMajor"), lambda self, value: self.setValue_forKey_(value, "versionMajor"))
'''.. attribute:: versionMajor
	:type: int'''
GSFont.versionMinor = property(lambda self: self.valueForKey_("versionMinor"), lambda self, value: self.setValue_forKey_(value, "versionMinor"))
'''.. attribute:: versionMinor
	:type: int'''
GSFont.date = property(lambda self: self.valueForKey_("date"), lambda self, value: self.setValue_forKey_(value, "date"))
'''.. attribute:: date
	:type: NSDate'''
GSFont.familyName = property(lambda self: self.valueForKey_("familyName"), 
							 lambda self, value: self.setFamilyName_(value))
'''.. attribute:: familyName
	Family name of the typeface.
	:type: unicode'''
GSFont.upm = property(lambda self: self.valueForKey_("unitsPerEm"), lambda self, value: self.setValue_forKey_(value, "unitsPerEm"))
'''.. attribute:: upm
	Units per Em
	:type: int'''
GSFont.note = property(lambda self: self.valueForKey_("note"), 
							 lambda self, value: self.setValue_forKey_(value, "note"))
'''.. attribute:: note
	:type: unicode'''
GSFont.kerning = property(lambda self: self.valueForKey_("kerning"), lambda self, value: self.setKerning_(value))
'''.. attribute:: kerning
	A multi-level dictionary. The first level's key is the :class:`GSFontMaster <GSFontMaster>`.id (each master has its own kerning), the second level's key is the :class:`GSGlyph <GSGlyph>`.id or class id (@MMK_L_XX), the third level's key is again a glyph id or class id (@MMK_R_XX). The values are the actual kerning values.
	
	To set a value, is is better to use the method Font.setKerningForPair(). This ensures a better data integrity (and is faster).
	:type: dict
'''
GSFont.userData = property(lambda self: self.pyobjc_instanceMethods.userData(), lambda self, value: self.setUserData_(value))
'''.. attribute:: userData
	A dictionary to store user data. Use a unique Key and only use object that can be stored in a Property list (string, list, dict, numbers, NSData) otherwise the date will not be recoverable from the saved file.
	:type: dict'''
GSFont.disablesNiceNames = property(lambda self: self.valueForKey_("disablesNiceNames").boolValue(), lambda self, value: self.setValue_forKey_(value, "disablesNiceNames"))
'''.. attribute:: disablesNiceNames
	Corresponds to the "Don't use nice names" setting from the Info dialogue.
	:type: bool'''
GSFont.customParameters = property(			lambda self: CustomParametersProxy(self))
'''.. attribute:: customParameters
	The custom parameters. You can access them by name or by index.::
		
		cp = GSCustomProperty("Test", "Test2")
		Font.customParameters.append(cp)
		
	or::
		
		Font.customParameters["Test"] = "Test2"

	Setting it by name might overwrite an existing property.
	
	:type: list, dict'''
GSFont.gridLength = property(lambda self: self.valueForKey_("gridLength").intValue(), lambda self, value: self.setValue_forKey_(value, "gridLength"))
'''.. attribute:: gridLength
	Corresponds to the "Grid spacing" setting from the Info dialogue. When set to 0, point positions may contains float values.
	:type: int'''

GSFont.selectedLayers = property(lambda self: self.parent.selectedLayers())
'''.. attribute:: selectedLayers
	Returns a list of all selected Layers in the active Tab.
	:type: list'''

GSFont.selectedFontMaster = property(lambda self: self.parent.selectedFontMaster())
'''.. attribute:: selectedFontMaster
	Returns the active Master (selected in the toolbar).
	:type: :class:`GSFontMaster <GSFontMaster>`'''

GSFont.masterIndex = property(lambda self: self.parent.masterIndex())
'''.. attribute:: masterIndex
	Returns the index of the active Master (selected in the toolbar).
	:type: int'''

def __current_Text__(self):
	try:
		return self.parent.windowController().activeEditViewController().graphicView().displayString()
	except:
		pass
	return None
def __set__current_Text__(self, String):
	#if String is None:
	#	String = ""
	self.parent.windowController().activeEditViewController().graphicView().setDisplayString_(String)

GSFont.currentText = property(lambda self: __current_Text__(self),
							  lambda self, value: __set__current_Text__(self, value))
'''.. attribute:: currentText
	The text of the current edit view. 
	
	Unencoded and none ASCII glyphs will use a slash and the glyph name. (e.g: /a.sc). Setting unicode strings works.
	
	:type: unicode'''

def Font_filepath(self):
	if self.parent is not None and self.parent.fileURL() is not None:
		return self.parent.fileURL().path()
	else:
		return None
GSFont.filepath = property(lambda self: Font_filepath(self))
'''.. attribute:: filepath
	On-disk location of GSFont object.
	:type: unicode'''

'''
---------
Functions
---------
'''


'''.. function:: disableUpdateInterface()
	
	Call this before you do big changes to the font, or to it's glyphs. Make sure that you call Font.enableUpdateInterface() when you are done.
	
	'''
'''.. function:: enableUpdateInterface()
	
	This reenables the interface update. Only makes sense to call if you have disabled it earlier.
	
	'''



def kerningForPair(self, FontMasterID, LeftKeringId, RightKerningId ):
	if not LeftKeringId[0] == '@':
		LeftKeringId = self.glyphs[LeftKeringId].id
	if not RightKerningId[0] == '@':
		RightKerningId = self.glyphs[RightKerningId].id
	return self.kerningForFontMasterID_LeftKey_RightKey_(FontMasterID, LeftKeringId, RightKerningId)
GSFont.kerningForPair = kerningForPair
'''.. function:: kerningForPair(FontMasterId, LeftKey, RightKey)
	
	This returns the kerning value for the two specified glyphs (LeftKey or RightKey is the glyphname) or a kerning group key (@MMK_X_XX).
	
	:param FontMasterId: The id of the FontMaster
	:type FontMasterId: str
	:param LeftKey: either a glyph name or a class name
	:type LeftKey: str
	:param RightKey: either a glyph name or a class name
	:type RightKey: str
	:return: The kerning value
	:rtype: float'''

def setKerningForPair(self, FontMasterID, LeftKeringId, RightKerningId, Value):
	if not LeftKeringId[0] == '@':
		LeftKeringId = self.glyphs[LeftKeringId].id
	if not RightKerningId[0] == '@':
		RightKerningId = self.glyphs[RightKerningId].id
	self.setKerningForFontMasterID_LeftKey_RightKey_Value_(FontMasterID, LeftKeringId, RightKerningId, Value)
GSFont.setKerningForPair = setKerningForPair
'''.. function:: setKerningForPair(FontMasterId, LeftKey, RightKey, Value)
	
	This sets the kerning for the two specified glyphs (LeftKey or RightKey is the glyphname) or a kerning group key (@MMK_X_XX).
	
	:param FontMasterId: The id of the FontMaster
	:type FontMasterId: str
	:param LeftKey: either a glyph name or a class name
	:type LeftKey: str
	:param RightKey: either a glyph name or a class name
	:type RightKey: str
	:param Value: kerning value
	:type Value: float'''

def removeKerningForPair(self, FontMasterID, LeftKeringId, RightKerningId):
	if LeftKeringId[0] != '@':
		try:
			LeftKeringId = self.glyphs[LeftKeringId].id
		except:
			pass
	if RightKerningId[0] != '@':
		try:
			RightKerningId = self.glyphs[RightKerningId].id
		except:
			pass
	self.removeKerningForFontMasterID_LeftKey_RightKey_(FontMasterID, LeftKeringId, RightKerningId)
GSFont.removeKerningForPair = removeKerningForPair
'''.. function:: removeKerningForPair(FontMasterId, LeftKey, RightKey)
	
	Removes the kerning for the two specified glyphs (LeftKey or RightKey is the glyphname) or a kerning group key (@MMK_X_XX).
	
	:param FontMasterId: The id of the FontMaster
	:type FontMasterId: str
	:param LeftKey: either a glyph name or a class name
	:type LeftKey: str
	:param RightKey: either a glyph name or a class name
	:type RightKey: str'''






##################################################################################
#
#
#
#           GSFontMaster
#
#
#
##################################################################################


'''

:mod:`GSFontMaster`
===============================================================================

Implementation of the master object. This corresponds with the "Masters" pane in the Font Info.

In Glyphs.app the glyphs of each master are reachable not here, but as :class:`Layers <GSLayer>` attached to the :class:`Glyphs <GSGlyph>` attached to the :class:`Font <GSFont>` object. See info graphic on top for better understanding.

.. class:: GSFontMaster

'''

def FontMaster__new__(typ, *args, **kwargs):
	return GSFontMaster.alloc().init()
GSFontMaster.__new__ = FontMaster__new__;

def FontMaster__init__(self):
	pass
GSFontMaster.__init__ = FontMaster__init__;

def FontMaster__repr__(self):
	return "<GSFontMaster \"%s\" width %s weight %s>" % (self.name, self.widthValue, self.weightValue)
GSFontMaster.__repr__ = FontMaster__repr__;

'''

.. autosummary::

	name
	id
	weight
	width
	weightValue
	widthValue
	customValue
	customName
	ascender
	capHeight
	xHeight
	descender
	italicAngle
	verticalStems
	horizontalStems
	alignmentZones
	guideLines
	userData
	customParameters

----------
Properties
----------

'''

GSFontMaster.id = property(lambda self: self.valueForKey_("id"), lambda self, value: self.setId_(value))
'''.. attribute:: id
	Used to identify :class:`Layers <GSLayer>` in the Glyph
	
	see :attr:`GSGlyph.layers <layers>`
	
	:type: unicode'''
GSFontMaster.name = property(lambda self: self.valueForKey_("name"), lambda self, value: self.setName_(value))
'''.. attribute:: name
	:type: string'''
GSFontMaster.weight = property(lambda self: self.valueForKey_("weight"), lambda self, value: self.setValue_forKey_(value, "weight"))
'''.. attribute:: weight
	:type: string'''
GSFontMaster.width = property(lambda self: self.valueForKey_("width"), lambda self, value: self.setValue_forKey_(value, "width"))
'''.. attribute:: width
	:type: string'''
GSFontMaster.weightValue = property(lambda self: self.valueForKey_("weightValue"), lambda self, value: self.setValue_forKey_(value, "weightValue"))
'''.. attribute:: weightValue
	Values for interpolation in design space.
	:type: float'''
GSFontMaster.widthValue = property(lambda self: self.valueForKey_("widthValue"), lambda self, value: self.setValue_forKey_(value, "widthValue"))
'''.. attribute:: widthValue
	Values for interpolation in design space.
	:type: float'''
GSFontMaster.customName = property(lambda self: self.valueForKey_("custom"), lambda self, value: self.setValue_forKey_(value, "custom"))
'''.. attribute:: customName
	The name of the custom interpolation dimension.
	:type: string'''
GSFontMaster.customValue = property(lambda self: self.valueForKey_("customValue"), lambda self, value: self.setValue_forKey_(value, "customValue"))
'''.. attribute:: customValue
	Values for interpolation in design space.'''
GSFontMaster.ascender = property(lambda self: self.valueForKey_("ascender"), lambda self, value: self.setValue_forKey_(value, "ascender"))
'''.. attribute:: ascender
	:type: float'''
GSFontMaster.capHeight = property(lambda self: self.valueForKey_("capHeight"), lambda self, value: self.setValue_forKey_(value, "capHeight"))
'''.. attribute:: capHeight
	:type: float'''
GSFontMaster.xHeight = property(lambda self: self.valueForKey_("xHeight"), lambda self, value: self.setValue_forKey_(value, "xHeight"))
'''.. attribute:: xHeight
	:type: float'''
GSFontMaster.descender = property(lambda self: self.valueForKey_("descender"), lambda self, value: self.setValue_forKey_(value, "descender"))
'''.. attribute:: descender
	:type: float'''
GSFontMaster.italicAngle = property(lambda self: self.valueForKey_("italicAngle"), lambda self, value: self.setValue_forKey_(value, "italicAngle"))
'''.. attribute:: italicAngle
	:type: float'''
GSFontMaster.verticalStems = property(lambda self: self.valueForKey_("verticalStems"), lambda self, value: self.setValue_forKey_(value, "verticalStems"))
'''.. attribute:: verticalStems
	The vertical stems. It is a list of numbers. 
	:type: list'''
GSFontMaster.horizontalStems = property(lambda self: self.valueForKey_("horizontalStems"), lambda self, value: self.setValue_forKey_(value, "horizontalStems"))
'''.. attribute:: horizontalStems
	The horizontal stems. It is a list of numbers. 
	:type: list'''
GSFontMaster.alignmentZones = property(lambda self: self.valueForKey_("alignmentZones"), lambda self, value: self.setValue_forKey_(value, "alignmentZones"))
#GSFontMaster.alignmentZones = property(lambda self: self.mutableArrayValueForKey_("alignmentZones"), lambda self, value: self.setValue_forKey_(value, "alignmentZones"))
'''.. attribute:: alignmentZones
	Collection of :class:`GSAlignmentZone <GSAlignmentZone>`.
	:type: list'''
GSFontMaster.guideLines = property(lambda self: self.valueForKey_("guideLines"), lambda self, value: self.setValue_forKey_(value, "guideLines"))
'''.. attribute:: guideLines
	Collection of :class:`GSGuideLine <GSGuideLine>`.
	:type: list'''
GSFontMaster.userData = property(lambda self: self.pyobjc_instanceMethods.userData(), lambda self, value: self.setValue_forKey_(value, "userData"))
'''.. attribute:: userData
	A dictionary to store user data. Use a unique Key and only use object that can be stored in a Property list (string, list, dict, numbers, NSData) otherwise the date will not be recoverable from the saved file.
	:type: dict'''
GSFontMaster.customParameters = property(lambda self: CustomParametersProxy(self))
'''.. attribute:: customParameters
	The custom parameters. You can access them by name or by index.::
	
		cp = GSCustomProperty("Test", "Test2")
		master.customParameters.append(cp)
	
	or::
	
		master.customParameters["Test"] = "Test2"
	
	Setting it by name might overwrite an existing property.
	
	:type: list, dict'''


##################################################################################
#
#
#
#           GSAlignmentZone
#
#
#
##################################################################################


'''
	
:mod:`GSAlignmentZone`
===============================================================================

Implementation of the alignmentZone object.

There is no distinction between Blue zones and other Zones. All negative zone (except the one with position 0) will be exported as Other zones.

The zone for the baseline should have position 0 (zero) and a negative width.

.. class:: GSAlignmentZone

	GSAlignmentZone([pos, size])
	
	:param pos: The position of the zone
	:param size: The size of the zone
'''

def AlignmentZone__new__(typ, *args, **kwargs):
	return GSAlignmentZone.alloc().init()
GSAlignmentZone.__new__ = AlignmentZone__new__;

def AlignmentZone__init__(self, pos = 0, size = 20):
	self.setPosition_(pos)
	self.setSize_(size)

GSAlignmentZone.__init__ = AlignmentZone__init__;

def AlignmentZone__repr__(self):
	#return "<GSAlignmentZone pos %s size %s>" % (self.position, self.size)
	return "<GSAlignmentZone pos %s size %s>" % (self.position(), self.size())
GSAlignmentZone.__repr__ = AlignmentZone__repr__;


'''
.. autosummary::

	position
	size
	
	
----------
Properties
----------
	
'''

GSAlignmentZone.size = property(lambda self: self.valueForKey_("size"), lambda self, value: self.setSize_(value))
'''.. attribute:: size
	
	:type: int
'''
GSAlignmentZone.position = property(lambda self: self.valueForKey_("position"), lambda self, value: self.setPosition_(value))
'''.. attribute:: position
	
	:type: int
	
	'''




##################################################################################
#
#
#
#           GSInstance
#
#
#
##################################################################################


'''

:mod:`GSInstance`
===============================================================================

Implementation of the instance object. This corresponds with the "Instances" pane in the Font Info.

.. class:: GSInstance

'''

def Instance__new__(typ, *args, **kwargs):
	return GSInstance.alloc().init()
GSInstance.__new__ = Instance__new__;

def Instance__init__(self):
	pass
GSInstance.__init__ = Instance__init__;

def Instance__repr__(self):
	return "<GSInstance \"%s\" width %s weight %s>" % (self.name, self.widthValue, self.weightValue)
GSInstance.__repr__ = Instance__repr__;


'''
.. autosummary::

	active
	name
	weight
	width
	weightValue
	widthValue
	customValue
	isItalic
	isBold
	linkStyle
	customParameters
	instanceInterpolations
	manualInterpolation
	
Functions
	
.. autosummary::
	
	generate()

----------
Properties
----------

'''

GSInstance.active = property(lambda self: self.valueForKey_("active").boolValue(), lambda self, value: self.setValue_forKey_(value, "active"))
'''.. attribute:: active
	:type: bool'''
GSInstance.name = property(lambda self: self.valueForKey_("name"), lambda self, value: self.setName_(value))
'''.. attribute:: name
	:type: string'''
GSInstance.weight = property(lambda self: self.valueForKey_("weightClass"), lambda self, value: self.setValue_forKey_(value, "weightClass"))
'''.. attribute:: weight
	:type: string'''
GSInstance.width = property(lambda self: self.valueForKey_("widthClass"), lambda self, value: self.setValue_forKey_(value, "widthClass"))
'''.. attribute:: width
	:type: string'''
GSInstance.weightValue = property(lambda self: self.valueForKey_("interpolationWeight"), lambda self, value: self.setValue_forKey_(value, "interpolationWeight"))
'''.. attribute:: weightValue
	Values for interpolation in design space.
	:type: float'''
GSInstance.widthValue = property(lambda self: self.valueForKey_("interpolationWidth"), lambda self, value: self.setValue_forKey_(value, "interpolationWidth"))
'''.. attribute:: widthValue
	Values for interpolation in design space.
	:type: float'''
GSInstance.customValue = property(lambda self: self.valueForKey_("interpolationCustom"), lambda self, value: self.setValue_forKey_(value, "interpolationCustom"))
'''.. attribute:: customValue
	Values for interpolation in design space.
	:type: float'''
GSInstance.isItalic = property(lambda self: self.valueForKey_("isItalic").boolValue(), lambda self, value: self.setValue_forKey_(value, "isItalic"))
'''.. attribute:: isItalic
	Italic flag for style linking
	:type: bool'''
GSInstance.isBold = property(lambda self: self.valueForKey_("isBold").boolValue(), lambda self, value: self.setValue_forKey_(value, "isBold"))
'''.. attribute:: isBold
	Bold flag for style linking
	:type: bool'''
GSInstance.linkStyle = property(lambda self: self.valueForKey_("linkStyle"), lambda self, value: self.setValue_forKey_(value, "linkStyle"))
'''.. attribute:: linkStyle
	Linked style
	:type: string'''
GSInstance.customParameters = property(lambda self: CustomParametersProxy(self))
'''.. attribute:: customParameters
	The custom parameters. You can access them by name or by index.::
	
		cp = GSCustomProperty("Test", "Test2")
		Instance.customParameters.append(cp)
	
	or::
	
		Instance.customParameters["Test"] = "Test2"
	
	Setting it by name might overwrite an existing property.
	
	:type: list, dict'''

GSInstance.instanceInterpolations = property(lambda self: self.pyobjc_instanceMethods.instanceInterpolations(), lambda self, value: self.setInstanceInterpolations_(value))
'''.. attribute:: instanceInterpolations
	A dict that contains the interpolation coefficents for each master.
	This is automatcially updated if you change interpolationWeight, interpolationWidth, interpolationCustom. It contains FontMaster IDs as keys and coeffients for that master as values.
	Or, you can set it maually if you set manualInterpolation to True. There is no UI for this, so you need to do that with a script.
	:type: dict
	'''

GSInstance.manualInterpolation = property(lambda self: self.valueForKey_("manualInterpolation"), lambda self, value: self.setValue_forKey_(value, "manualInterpolation"))
'''.. attribute:: manualInterpolation
	Disables automatic calculation of instanceInterpolations
	
	This allowes to manually setting of instanceInterpolations
	:type: bool
	'''


'''
---------
Functions
---------


.. function:: generate(Format = "OTF", FontPath = None, AutoHint = True, RemoveOverlap = True, UseSubroutines = True, UseProductionNames = True)
	
	exports the instance
	
	:param str Format: 'OTF' or 'TTF'
	:param str FontPath: The destination path for the final fonts. If None, it uses the default location set in the export dialog
	:param bool AutoHint: If autohinting should be applied. Default: True
	:param bool RemoveOverlap: If overlaps should be removed. Default: True
	:param bool UseSubroutines: If to use subroutines for CFF. Default: True
	:param bool UseProductionNames: If to use production names. Default: True
	:return: On success, True, on failure error message.
	:rtype: bool/list
'''

class _ExporterDelegate_ (NSObject):
	def init(self):
		self = super(_ExporterDelegate_, self).init()
		self.result = True
		return self
	
	def collectResults_(self, Error): # Error might be a NSString or a NSError
		if Error.__class__.__name__ == "NSError":
			String = Error.localizedDescription()
			if Error.localizedRecoverySuggestion().length() > 0:
				String = String.stringByAppendingString_(Error.localizedRecoverySuggestion())
			Error = unicode(String)
		self.result = Error

def __Instance_Export__(self, Format = "OTF", FontPath = None, AutoHint = True, RemoveOverlap = True, UseSubroutines = True, UseProductionNames = True):
	
	if Format == "OTF":
		Format = 0
	else:
		Format = 1 # 0 == OTF, 1 = TTF
	Font = self.font()
	Exporter = NSClassFromString("GSExportInstanceOperation").alloc().initWithFont_instance_format_(Font, self, Format)
	if FontPath is None:
		FontPath = NSUserDefaults.standardUserDefaults().objectForKey_("OTFExportPath")

	Exporter.setInstallFontURL_(NSURL.fileURLWithPath_(FontPath))
	# die folgenden Parameter kann man hier direkt setzen oder die werden aus der Instanz ausgelesen.
	Exporter.setAutohint_(AutoHint)
	Exporter.setRemoveOverlap_(RemoveOverlap)
	Exporter.setUseSubroutines_(UseSubroutines)
	Exporter.setUseProductionNames_(UseProductionNames)

	Exporter.setTempPath_(os.path.expanduser("~/Library/Application Support/Glyphs/Temp/")) # this has to be set correctly.

	Delegate = _ExporterDelegate_.alloc().init() # the collectResults_() method of this object will be called on case the exporter has to report a problem.
	Exporter.setDelegate_(Delegate)
	Exporter.main()
	return Delegate.result

GSInstance.generate = __Instance_Export__




##################################################################################
#
#
#
#           GSCustomProperty
#
#
#
##################################################################################


'''
	
:mod:`GSCustomProperty`
===============================================================================

Implementation of the Custom Property object.

It stores a name/value pair

.. class:: GSCustomProperty
	
	GSCustomProperty([name, value])
	
	:param name: The name
	:param size: The value
'''

def CustomProperty__new__(typ, *args, **kwargs):
	return GSCustomProperty.alloc().init()

GSCustomProperty.__new__ = CustomProperty__new__;

def CustomProperty__init__(self, name, value):
	self.setName_(name)
	self.setValue_(value)

GSCustomProperty.__init__ = CustomProperty__init__;

def CustomProperty__repr__(self):
	return "<GSCustomProperty %s = %s>" % (self.name, self.value)
GSCustomProperty.__repr__ = CustomProperty__repr__;


'''
	.. autosummary::
	
	name
	value
	
	
----------
Properties
----------
	
	'''

GSCustomProperty.name = property(lambda self: self.valueForKey_("name"), lambda self, value: self.setName_(value))
'''.. attribute:: name
	
	:type: str
	'''
GSCustomProperty.value = property(lambda self: self.valueForKey_("value"), lambda self, value: self.setValue_(value))
'''.. attribute:: value
	
	:type: str, list, dict, int, float
	
	'''










##################################################################################
#
#
#
#           GSClass
#
#
#
##################################################################################

'''
:mod:`GSClass`
===============================================================================

Implementation of the class object. It is used to store OpenType classes.

.. class:: GSClass

	GSClass([tag, code])
	
	:param tag: The class name
	:param code: A list of glyph names, separated by space or newline

Properties

.. autosummary::

	name
	code
	automatic

----------
Properties
----------

'''

def Class__new__(typ, *args, **kwargs):
	return GSClass.alloc().init()
GSClass.__new__ = Class__new__;

def Class__init__(self, name = None, code = None):
	if name is not None:
		self.setName_(name)
	if code is not None:
		self.setCode_(code)
GSClass.__init__ = Class__init__;

def Class__repr__(self):
	return "<GSClass \"%s\">" % (self.name)
GSClass.__repr__ = Class__repr__;

GSClass.name = property(lambda self: self.valueForKey_("name"), 
							 lambda self, value: self.setName_(value))
'''.. attribute:: name
	The Class name
	:type: unicode'''
GSClass.code = property(lambda self: self.valueForKey_("code"), 
							 lambda self, value: self.setCode_(value))
'''.. attribute:: code
	A String with space separated glyph names.
	:type: unicode
'''
GSClass.automatic = property(lambda self: self.valueForKey_("automatic").boolValue(), 
							 lambda self, value: self.setAutomatic_(value))
'''.. attribute:: automatic
	Auto-generate this class
	:type: bool
'''



##################################################################################
#
#
#
#           GSFeaturePrefix
#
#
#
##################################################################################

'''
:mod:`GSFeaturePrefix`
===============================================================================
	
Implementation of the featurePrefix object. It is used to store things that need to be outside of a feature like standalone lookups.
	
.. class:: GSFeaturePrefix

	GSFeaturePrefix([tag, code])
	
	:param tag: The Prefix name
	:param code: The feature code in Adobe FDK syntax
	
Properties

.. autosummary::

	name
	code
	automatic

----------
Properties
----------
	
	'''

def FeaturePrefix__new__(typ, *args, **kwargs):
	return GSFeaturePrefix.alloc().init()
GSFeaturePrefix.__new__ = FeaturePrefix__new__;

def FeaturePrefix__init__(self, name = None, code = None):
	if name is not None:
		self.setName_(name)
	if code is not None:
		self.setCode_(code)

GSFeaturePrefix.__init__ = FeaturePrefix__init__;

def FeaturePrefix__repr__(self):
	return "<GSFeaturePrefix \"%s\">" % (self.name)
GSFeaturePrefix.__repr__ = FeaturePrefix__repr__;

GSFeaturePrefix.name = property(lambda self: self.valueForKey_("name"),
						lambda self, value: self.setName_(value))
'''.. attribute:: name
	The FeaturePrefix name
	:type: unicode'''
GSFeaturePrefix.code = property(lambda self: self.valueForKey_("code"),
						lambda self, value: self.setCode_(value))
'''.. attribute:: code
	A String containing feature code.
	:type: unicode
	'''
GSFeaturePrefix.automatic = property(lambda self: self.valueForKey_("automatic").boolValue(),
							 lambda self, value: self.setAutomatic_(value))
'''.. attribute:: automatic
	Auto-generate this FeaturePrefix
	:type: bool
	'''






##################################################################################
#
#
#
#           GSFeature
#
#
#
##################################################################################

'''

:mod:`GSFeature`
===============================================================================

.. class:: GSFeature

	Implementation of the feature object. It is used to implement OpenType Features in the Font Info.
	
	GSFeature([tag, code])
	
	:param tag: The feature name
	:param code: The feature code in Adobe FDK syntax
	
Properties

.. autosummary::

	name
	code
	automatic
	notes
	
Functions

.. autosummary::

	update()
	

----------
Properties
----------

'''


def Feature__new__(typ, *args, **kwargs):
	#print "new", args, kwargs
	return GSFeature.alloc().init()
GSFeature.__new__ = Feature__new__;

def Feature__init__(self, name = None, code = None):
	if name is not None:
		self.setName_(name)
	if code is not None:
		self.setCode_(code)
	
GSFeature.__init__ = Feature__init__;

def Feature__repr__(self):
	return "<GSFeature \"%s\">" % (self.name)
GSFeature.__repr__ = Feature__repr__;

GSFeature.name = property(lambda self: self.valueForKey_("name"), 
								 lambda self, value: self.setName_(value))
'''.. attribute:: name
	The feature name
	:type: unicode'''

GSFeature.code = property(lambda self: self.valueForKey_("code"), 
								 lambda self, value: self.setCode_(value))
'''.. attribute:: code
	The Feature code in Adobe FDK syntax.
	:type: unicode'''
GSFeature.automatic = property(lambda self: self.valueForKey_("automatic").boolValue(), 
								 lambda self, value: self.setAutomatic_(value))
'''.. attribute:: automatic
	Auto-generate this feature
	:type: bool
'''

GSFeature.notes = property(lambda self: self.valueForKey_("notes"),
							   lambda self, value: self.setNotes_(value))
'''.. attribute:: notes
	Some extra text. Is shown in the bottom of the feature window. Contains the stylistic set name parameter
	:type: unicode
	'''

'''

---------
Functions
---------


'''

'''.. function:: update()
	
	Calls the automatic feature code generator for this feature.
	
	:return: None
'''











##################################################################################
#
#
#
#           GSSubstitution
#
#
#
##################################################################################


"""

############ NOCH NICHT DOKUMENTIERT WEIL NOCH NICHT AUSGEREIFT ############ 

"""


def Substitution__new__(typ, *args, **kwargs):
	return GSSubstitution.alloc().init()
GSSubstitution.__new__ = Substitution__new__;

def Substitution__init__(self):
	pass
GSSubstitution.__init__ = Substitution__init__;


GSSubstitution.source = property(lambda self: self.valueForKey_("back"), 
								 lambda self, value: self.setBack_(value))
GSSubstitution.source = property(lambda self: self.valueForKey_("source"), 
								 lambda self, value: self.setSource_(value))
GSSubstitution.forward = property(lambda self: self.valueForKey_("fwd"), 
								 lambda self, value: self.setFwd_(value))

GSSubstitution.target = property(lambda self: self.valueForKey_("target"), 
								 lambda self, value: self.setTarget_(value))
GSSubstitution.languageTag = property(lambda self: self.valueForKey_("languageTag"), 
								 lambda self, value: self.setLanguageTag_(value))
GSSubstitution.scriptTag = property(lambda self: self.valueForKey_("scriptTag"), 
								 lambda self, value: self.setScriptTag_(value))











##################################################################################
#
#
#
#           GSGlyph
#
#
#
##################################################################################

'''


:mod:`GSGlyph`
===============================================================================

.. class:: GSGlyph

	Implementation of the glyph object.

	GSGlyph([name])

	:param name: The glyph name
	
	
	
**Properties**
	
.. autosummary::

	parent
	layers
	name
	unicode
	string
	id
	category
	subCategory
	script
	leftKerningGroup
	rightKerningGroup
	leftMetricsKey
	rightMetricsKey
	export
	color
	note
	selected
	
**Functions**

.. autosummary::

	beginUndo()
	endUndo()

----------
Properties
----------
	
'''


def Glyph__new__(typ, *args, **kwargs):
	return GSGlyph.alloc().init()
GSGlyph.__new__ = Glyph__new__;

def Glyph__init__(self, name=None):
	if name and (isinstance(name, str) or isinstance(name, unicode)):
		self.setName_(name)
GSGlyph.__init__ = Glyph__init__;

def Glyph__repr__(self):
	return "<GSGlyph \"%s\" with %s layers>" % (self.name, len(self.layers))
GSGlyph.__repr__ = Glyph__repr__;

GSGlyph.parent = property(			lambda self: self.valueForKey_("parent"),
									lambda self, value: self.setParent_(value)) 
'''.. attribute:: parent
	Reference to the :class:`Font <GSFont>` object.

	:type: :class:`GSFont <GSFont>`
'''
GSGlyph.layers = property(			lambda self: GlyphLayerProxy(self))

'''.. attribute:: layers
	The layers of the glyph, collection of :class:`GSLayer <GSLayer>` objects. You can access them either by index or by :attr:`GSFontMaster.id <id>`.
	
	To access a layer, use the master ID:
	.. code-block:: python
		master = font.masters[0]
		print glyph.layers[master.id]
		<GSLayer "Light" (A)>

	:type: list, dict
'''
GSGlyph.name = property(			lambda self: self.pyobjc_instanceMethods.name(),
									lambda self, value: self.setName_(value))
'''.. attribute:: name
	The name of the glyph. It will be converted to a "nice name" (afii10017 to A-cy) (you can disable this behavior in font info or the app preference)
	:type: unicode
'''

GSGlyph.unicode = property(			lambda self: self.pyobjc_instanceMethods.unicode() )
'''.. attribute:: unicode
	String with Unicode value of glyph, if encoded.
	Read only.
	:type: unicode
'''

def _get_Glyphs_String(self):
	if self.unicode:
		return unichr(int(self.unicode, 16))

GSGlyph.string =		  property( lambda self: _get_Glyphs_String(self))

'''.. attribute:: string
	String representation of glyph, if encoded.
	This is similar to the string representation that you get when copying glyphs into the clipboard.
	:type: unicode
'''
GSGlyph.id = property(				lambda self: str(self.valueForKey_("id")),
									lambda self, value: self.setId_(value))
'''.. attribute:: id
	An unique identifier for each glyph
	:type: unicode'''
GSGlyph.category = property(		lambda self: self.valueForKey_("category"))
'''.. attribute:: category
	The category of the glyph. e.g. 'Letter', 'Symbol'
	:type: unicode
'''
GSGlyph.subCategory = property(		lambda self: self.valueForKey_("subCategory"))
'''.. attribute:: subCategory
	The subCategory of the glyph. e.g. 'Uppercase', 'Math'
	:type: unicode
'''
GSGlyph.script = property(			lambda self: self.valueForKey_("script"))
'''.. attribute:: script
	The script of the glyph, e.g. 'latin', 'arabic'.
	:type: unicode
'''
GSGlyph.leftKerningGroup = property(lambda self: self.valueForKey_("leftKerningGroup"), 
									lambda self, value: self.setLeftKerningGroup_(value))
'''.. attribute:: leftKerningGroup
	The leftKerningGroup of the glyph. All glyphs with the same text in the kerning group end up in the same kerning class.
	:type: unicode'''
GSGlyph.rightKerningGroup = property(lambda self: self.valueForKey_("rightKerningGroup"), 
									lambda self, value: self.setRightKerningGroup_(value))
'''.. attribute:: rightKerningGroup
	The rightKerningGroup of the glyph. All glyphs with the same text in the kerning group end up in the same kerning class.
	:type: unicode'''
GSGlyph.leftMetricsKey =  property(	lambda self: self.valueForKey_("leftMetricsKey"), 
									lambda self, value: self.setLeftMetricsKey_(value))
'''.. attribute:: leftMetricsKey
	The leftMetricsKey of the glyph. This is a reference to another glyph by name. It is used to synchronize the metrics with the linked glyph.
	:type: unicode'''
GSGlyph.rightMetricsKey = property(	lambda self: self.valueForKey_("rightMetricsKey"), 
									lambda self, value: self.setRightMetricsKey_(value))
'''.. attribute:: rightMetricsKey
	The rightMetricsKey of the glyph. This is a reference to another glyph by name. It is used to synchronize the metrics with the linked glyph.
	:type: unicode'''
GSGlyph.export =		  property( lambda self: self.valueForKey_("export").boolValue(), 
									lambda self, value: self.setExport_(value))

'''.. attribute:: export
	Glyphs should export upon font generation
	:type: bool'''

GSGlyph.color =			  property( lambda self: self.valueForKey_("colorIndex"), 
									lambda self, value: self.setColorIndex_(value))
'''.. attribute:: color
	Color marking of glyph in UI
	:type: int'''

GSGlyph.note =			  property( lambda self: self.valueForKey_("note"), 
									lambda self, value: self.setNote_(value))
'''.. attribute:: note
	:type: unicode'''

def _get_Glyphs_is_selected(self):
	Doc = self.parent.parent
	return Doc.windowController().glyphsController().selectedObjects().containsObject_(self)

def _set_Glyphs_is_selected(self, isSelected):
	ArrayController = self.parent.parent.windowController().glyphsController()
	if isSelected:
		ArrayController.addSelectedObjects_([self])
	else:
		ArrayController.removeSelectedObjects_([self])

GSGlyph.selected =		property( lambda self: _get_Glyphs_is_selected(self),
								  lambda self, value: _set_Glyphs_is_selected(self, value))
'''.. attribute:: selected
	Return True if the Glyph is selected in the Font View. 
	This is different to the property font.selectedLayers as this returns the selection from the active tab.
	:type: bool'''

def __BeginUndo(self):
	self.undoManager().beginUndoGrouping()

GSGlyph.beginUndo = __BeginUndo

'''.. function:: beginUndo()
	
	Call this before you do a longer running change to the glyph. Be extra careful to call Glyph.endUndo() when you are finished.
'''

def __EndUndo(self):
	self.undoManager().endUndoGrouping()

GSGlyph.endUndo = __EndUndo

'''.. function:: endUndo()
	
	This closes a undo group that was opened by a previous call of Glyph.beginUndo(). Make sure that you call this for each beginUndo() call.
'''

##################################################################################
#
#
#
#           GSLayer
#
#
#
##################################################################################


'''

:mod:`GSLayer`
===============================================================================

.. class:: GSLayer

Implementation of the layer object

**Properties**

.. autosummary::
	
	parent
	name
	associatedMasterId
	layerId
	components
	guides
	hints
	anchors
	paths
	LSB
	RSB
	TSB
	BSB
	width
	bounds
	background

**Functions**

.. autosummary::
	
	decomposeComponents
	compareString
	connectAllOpenPaths
	copyDecomposedLayer
	syncMetrics
	correctPathDirection
	removeOverlap
	beginChanges
	endChanges
	cutBetweenPoints
	intersectionsBetweenPoints

----------
Properties
----------

	
	'''

def Layer__new__(typ, *args, **kwargs):
	return GSLayer.alloc().init()
GSLayer.__new__ = Layer__new__;

def Layer__init__(self):
	pass
GSLayer.__init__ = Layer__init__;

def Layer__repr__(self):
	return "<%s \"%s\" (%s)>" % (self.className(), self.name, self.parent.name)
GSLayer.__repr__ = Layer__repr__;

GSLayer.parent = property(			lambda self: self.valueForKey_("parent"),
									lambda self, value: self.setParent_(value))
GSBackgroundLayer.parent = property(lambda self: self.valueForKey_("parent"),
									lambda self, value: self.setParent_(value))
'''.. attribute:: parent
	Reference to the :class:`Glyph <GSGlyph>` object.
	:type: :class:`GSGlyph <GSGlyph>`
'''

GSLayer.name = property(			lambda self: self.valueForKey_("name"),
									lambda self, value: self.setName_(value)) 
'''.. attribute:: name
	Name of layer
	:type: unicode'''

GSLayer.associatedMasterId = property(lambda self: self.valueForKey_("associatedMasterId"),
									lambda self, value: self.setAssociatedMasterId_(value)) 
'''.. attribute:: associatedMasterId
	The ID of the :class:`FontMaster <GSFontMaster>` this layer belongs to.
	:type: unicode'''
GSLayer.layerId = property(lambda self: self.valueForKey_("layerId"),
									  lambda self, value: self.setLayerId_(value)) 
'''.. attribute:: layerId
	The layer key is used to access the layer in the :class:`glyphs <GSGlyph>` layer dictionary.
	
	For master layers this should be the id of the :class:`FontMaster <GSFontMaster>`.
	It could look like this: "FBCA074D-FCF3-427E-A700-7E318A949AE5"
	:type: unicode'''

GSLayer.components = property(lambda self: LayerComponentsProxy(self),
							  lambda self, value: self.setComponents_(NSMutableArray.arrayWithArray_(value)))
'''.. attribute:: components
	Collection of :class:`GSComponent` objects
	:type: list
'''

GSLayer.guideLines = property(lambda self: LayerGuideLinesProxy(self),
							  lambda self, value: self.setGuideLines_(NSMutableArray.arrayWithArray_(value)))

GSLayer.guides = property(lambda self: LayerGuideLinesProxy(self),
							  lambda self, value: self.setGuideLines_(NSMutableArray.arrayWithArray_(value)))
'''.. attribute:: guides
	List of :class:`GSGuideLine` objects.
	:type: list
'''

GSLayer.hints = property(lambda self: LayerHintsProxy(self),
						 lambda self, value: self.setHints_(value))
'''.. attribute:: hints
	List of :class:`GSHint` objects.
	:type: list
'''

GSLayer.anchors = property(lambda self: LayerAnchorsProxy(self))
'''.. attribute:: anchors
	List of :class:`GSAnchor` objects.
	:type: dict
'''

GSLayer.paths = property(	lambda self: LayerPathsProxy(self),
						 lambda self, value: self.setPaths_(NSMutableArray.arrayWithArray_(value)))
'''.. attribute:: paths
	List of :class:`GSPath <GSPath>` objects.
	:type: list
'''
	
GSLayer.LSB = property(		lambda self: self.valueForKey_("LSB").floatValue(),
							lambda self, value: self.setLSB_(float(value)))
'''.. attribute:: LSB
	Left sidebearing
	:type: float
'''

GSLayer.RSB = property(		lambda self: self.valueForKey_("RSB").floatValue(),
							lambda self, value: self.setRSB_(float(value)))
'''.. attribute:: RSB
	Right sidebearing
	:type: float'''

GSLayer.TSB = property(		lambda self: self.valueForKey_("TSB").floatValue(),
							lambda self, value: self.setTSB_(float(value)))
'''.. attribute:: TSB
	Top sidebearing
	:type: float'''

GSLayer.BSB = property(		lambda self: self.valueForKey_("BSB").floatValue(),
							lambda self, value: self.setBSB_(float(value)))
'''.. attribute:: BSB
	Bottom sidebearing
	:type: float'''

GSLayer.width = property(	lambda self: self.valueForKey_("width").floatValue(),
							lambda self, value: self.setWidth_(float(value)))
'''.. attribute:: width
	Glyph width
	:type: float'''

GSLayer.bounds = property(	lambda self: self.pyobjc_instanceMethods.bounds() )

'''.. attribute:: bounds
	Bounding box as NSRect (origin and size). Read-only.
	:type: NSRect'''

GSLayer.background = property(lambda self: self.pyobjc_instanceMethods.background())

'''.. attribute:: background
	The background layer
	:type: :class:`GSLayer <GSLayer>`'''

'''

---------
Functions
---------

.. function:: decomposeComponents()
	
	Decomposes all components of the layer at once.

.. function:: compareString()
	
	Returns a string representing the outline structure of the glyph, for compatibility comparison.

	:return: The comparison string

	:rtype: string

.. function:: connectAllOpenPaths()
	
	Closes all open paths when end points are further than 1 unit away from each other.


.. function:: copyDecomposedLayer()
	
	Returns a copy of the layer with all components decomposed.

	:return: A new layer object

	:rtype: :class:`GSLayer <GSLayer>`

.. function:: syncMetrics()
	
	Take over LSB and RSB from linked glyph.

.. function:: correctPathDirection()
	
	Corrects the path direction.

.. function:: removeOverlap()
	
	Joins all contours.

.. function:: beginChanges()

	Call this before you do bigger changes to the Layer.
	This will increase performance and prevent undo problems.
	Always call layer.endChanges() if you are finished.

.. function:: endChanges()

	Call this if you have called layer.beginChanges before. Make sure to group bot calls properly.
	
.. function:: cutBetweenPoints(Point1, Point2)

	Cuts all paths that intersect the line from Point1 to Point2
	
	:param Point1: one point
	:param Point2: the other point

.. function:: intersectionsBetweenPoints(Point1, Point2)

	Cuts all paths that intersect the line from Point1 to Point2
	
	:param Point1: one point
	:param Point2: the other point

	available in Glyphs 2, 683
'''

def RemoveOverlap(self):
	removeOverlapFilter = NSClassFromString("GlyphsFilterRemoveOverlap").alloc().init()
	removeOverlapFilter.runFilterWithLayer_error_(self, None)

GSLayer.removeOverlap = RemoveOverlap

def BeginChanges(self):
	self.setDisableUpdates()
	self.undoManager().beginUndoGrouping()
GSLayer.beginChanges = BeginChanges

def EndChanges(self):
	self.setEnableUpdates()
	self.undoManager().endUndoGrouping()
GSLayer.endChanges = EndChanges

def CutBetweenPoints(self, Point1, Point2):
	GlyphsToolOther = NSClassFromString("GlyphsToolOther")
	GlyphsToolOther.cutPathsInLayer_forPoint_endPoint_(self, Point1, Point2)
GSLayer.cutBetweenPoints = CutBetweenPoints

def IntersectionsBetweenPoints(self, Point1, Point2):
	return self.calculateIntersectionsStartPoint_endPoint_(Point1, Point2)
GSLayer.intersectionsBetweenPoints = IntersectionsBetweenPoints



def DrawLayerWithPen(self, pen):
	"""draw the object with a RoboFab segment pen"""
	try:
		pen.setWidth(self.width)
		if self.note is not None:
			pen.setNote(self.note)
	except AttributeError:
		# FontTools pens don't have these methods
		pass
	for a in self.anchors:
		a.draw(pen)
	for c in self.paths:
		c.draw(pen)
	for c in self.components:
		c.draw(pen)
	try:
		pen.doneDrawing()
	except AttributeError:
		# FontTools pens don't have a doneDrawing() method
		pass

GSLayer.draw = DrawLayerWithPen

def DrawPointsWithPen(self, pen):
	"""draw the object with a point pen"""
	for a in self.anchors:
		a.drawPoints(pen)
	for c in self.paths:
		c.drawPoints(pen)
	for c in self.components:
		c.drawPoints(pen)

GSLayer.drawPoints = DrawPointsWithPen

def _Clear_(self, contours=True, components=True, anchors=True, guides=True):
	"""Clear all items marked as True from the glyph"""
	if contours:
		self.setPaths_(NSMutableArray.array())
	# if components:
	# 	self.clearComponents()
	# if anchors:
	# 	self.clearAnchors()
	# if guides:
	# 	self.clearHGuides()
	# 	self.clearVGuides()

GSLayer.clear = _Clear_

def _getPen_(self):
	return GSPathPen.alloc().init()

GSLayer.getPen = _getPen_

def _getPointPen_(self):
	#print "Get GSPoint Pen"
	if "GSPen" in sys.modules.keys():
		del(sys.modules["GSPen"])
	from GSPen import GSPointPen
	
	return GSPointPen(self, self)

GSLayer.getPointPen = _getPointPen_

def _invalidateContours_(self):
	pass

GSLayer._invalidateContours = _invalidateContours_

##################################################################################
#
#
#
#           GSAnchor
#
#
#
##################################################################################

'''

:mod:`GSAnchor`
===============================================================================

.. class:: GSAnchor <GSElement>

Implementation of the anchor object.

.. function::GSAnchor([name, pt])

	:param name: the name of the anchor
	:param pt: the position of the anchor

.. autosummary::
	
	position
	name
	

----------
Properties
----------

'''


def Anchor__new__(typ, *args, **kwargs):
	return GSAnchor.alloc().init()
GSAnchor.__new__ = Anchor__new__;

def Anchor__init__(self, name = None, pt = None):
	if pt:
		self.setPosition_(pt)
	if name:
		self.setName_(name)
GSAnchor.__init__ = Anchor__init__;

def Anchor__repr__(self):
	return "<GSAnchor \"%s\" x=%s y=%s>" % (self.name, self.position.x, self.position.y)
GSAnchor.__repr__ = Anchor__repr__;

GSAnchor.position = property(	lambda self: self.valueForKey_("position").pointValue(),
								lambda self, value: self.setPosition_(value))
'''.. attribute:: position
	The position of the anchor
	:type: NSPoint'''

GSAnchor.name = property(		lambda self: self.valueForKey_("name"),
								lambda self, value: self.setName_(value))
'''.. attribute:: name
	The name of the anchor
	:type: unicode'''

def DrawAnchorWithPen(self, pen):
	pen.moveTo(self.position)
	pen.endPath()

GSAnchor.draw = DrawAnchorWithPen






##################################################################################
#
#
#
#           GSComponent
#
#
#
##################################################################################


'''

:mod:`GSComponent`
===============================================================================

.. class:: GSComponent
	
	Implementation of the component object.

	GSComponent(glyph [, pt] )

	:param glyph: a glyph object or the glyph name
	:param pt: the position of the component

**Properties**

.. autosummary::
	
	position
	componentName
	component
	transform
	bounds
	
**Functions**

.. autosummary::
	
	decompose

	
----------
Properties
----------

	'''

def Component__new__(typ, *args, **kwargs):
	return GSComponent.alloc().init()
GSComponent.__new__ = Component__new__;

def Component__init__(self, glyph, offset=(0,0), scale=(1,1), transform=None):
	"""
	transformation: transform matrix as list of numbers
	"""
	if transform is None:
		xx, yy = scale
		dx, dy = offset
		self.transform = (xx, 0, 0, yy, dx, dy)
	else:
		self.transform = transform
		
	if glyph:
		if isinstance(glyph, (str, unicode)):
			self.setComponentName_(glyph)
		elif isinstance(glyph, GSGlyph):
			self.setComponentName_(glyph.name)
		elif isinstance(glyph, "RGlyph"):
			self.setComponentName_(glyph.name)

GSComponent.__init__ = Component__init__;

def Component__repr__(self):
	return "<GSComponent \"%s\" x=%s y=%s>" % (self.componentName, self.position.x, self.position.y)
GSComponent.__repr__ = Component__repr__;

GSComponent.position = property(	lambda self: self.valueForKey_("position").pointValue(),
									lambda self, value: self.setPosition_(value))
'''.. attribute:: position
	The Position of the component.
	:type: NSPoint'''

GSComponent.componentName = property(lambda self: self.valueForKey_("componentName"),
									lambda self, value: self.setComponentName_(value))
'''.. attribute:: componentName
	The glyph name the component is pointing to.
	:type: unicode'''

GSComponent.component = property(	lambda self: self.valueForKey_("component"))
'''.. attribute:: component
	The :class:`GSGlyph <GSGlyph>` the component is pointing to. This is read only. Set the componentName to the glyph name.
	:type: :class:`GSGlyph <GSGlyph>`
'''

GSComponent.transform = property(	lambda self: self.transformStruct(),
									lambda self, value: self.setTransformStruct_(value))
'''.. attribute:: transform
	
	:type: NSAffineTransformStruct'''

GSComponent.bounds = property(		lambda self: self.pyobjc_instanceMethods.bounds() )
'''.. attribute:: bounds
	
	Bounding box of the component, read only
	
	:type: NSRect'''

GSComponent.disableAlignment = property(lambda self: self.pyobjc_instanceMethods.disableAlignment(),
									lambda self, value: self.setDisableAlignment_(value))
'''.. attribute:: disableAlignment
	
	defines if the component is automatically aligned
	
	:type: bool'''

def DrawComponentWithPen(self, pen):
	pen.addComponent(self.componentName, self.transform)

GSComponent.draw = DrawComponentWithPen

'''


----------
Functions
----------

'''

'''.. function:: decompose()
	
	Decomposes the component
'''






##################################################################################
#
#
#
#           GSPath
#
#
#
##################################################################################


'''

:mod:`GSPath`
===============================================================================

Implementation of the path object.

If you build a path in code, make sure that the structure isvalid. A curve node has the be preceded by two off-curve nodes. And an open path has to start with a line node.

.. class:: GSPath

**Properties**

.. autosummary::
	
	parent
	nodes
	segments
	closed
	direction
	bounds
	
**Functions**

.. autosummary::
	
	reverse

----------
Properties
----------

	
'''


def Path__new__(typ, *args, **kwargs):
	return GSPath.alloc().init()
GSPath.__new__ = Path__new__;

def Path__init__(self):
	pass
GSPath.__init__ = Path__init__;

def Path__repr__(self):
	return "<GSPath %s nodes and %s segments>" % (len(self.nodes), len(self.segments))
GSPath.__repr__ = Path__repr__;

GSPath.parent = property(		lambda self: self.valueForKey_("parent"),
								lambda self, value: self.setParent_(value)) 
'''.. attribute:: parent
	Reference to the :class:`Layer <GSLayer>` object.

	:type: :class:`GSLayer <GSLayer>`
'''

GSPath.nodes = property(		lambda self: PathNodesProxy(self),
								lambda self, value: self.setNodes_(NSMutableArray.arrayWithArray_(value)))
'''.. attribute:: nodes
	A list of :class:`GSNode <GSNode>` objects
	:type: list'''
	
GSPath.segments = property(		lambda self: self.valueForKey_("segments"),
						 		lambda self, value: self.setSegments_(value))
'''.. attribute:: segments
	A list of segments as NSPoint objects. Two objects represent a line, four represent a curve. Start point of the segment is included.
	:type: list'''

GSPath.closed = property(		lambda self: self.valueForKey_("closed").boolValue(),
						 		lambda self, value: self.setValue_forKey_(value, "closed"))
'''.. attribute:: closed
	Returns True if the the path is closed
	:type: bool'''

GSPath.direction = property(		lambda self: self.valueForKey_("direction"))
'''.. attribute:: direction
	Path direction. -1 for counter clockwise, 1 for clockwise.
	:type: int'''

GSPath.bounds = property(	 lambda self: self.pyobjc_instanceMethods.bounds() )
'''.. attribute:: bounds
	Bounding box of the path, read only
	:type: NSRect'''

'''

----------
Functions
----------

.. function:: reverse()
	
	Reverses the path direction
'''

def DrawPathWithPen(self, pen):
	"""draw the object with a fontTools pen"""
	
	Start = 0
	if self.closed:
		for i in range(len(self)-1, -1, -1):
			StartNode = self.nodeAtIndex_(i)
			if StartNode.type is not GSOFFCURVE:
				pen.moveTo(StartNode.position)
				break
	else:
		for i in range(len(self)):
			StartNode = self.nodeAtIndex_(i)
			if StartNode.type is not GSOFFCURVE:
				pen.moveTo(StartNode.position)
				Start = i + 1
				break
	for i in range(Start, len(self), 1):
		Node = self.nodeAtIndex_(i)
		if Node.type == GSLINE:
			pen.lineTo(Node.position)
		elif Node.type == GSCURVE:
			pen.curveTo(self.nodeAtIndex_(i-2).position, self.nodeAtIndex_(i-1).position, Node.position)
	if self.closed:
		pen.closePath()
	else:
		pen.endPath()
	return

GSPath.draw = DrawPathWithPen








##################################################################################
#
#
#
#           GSNode
#
#
#
##################################################################################

'''

:mod:`GSNode`
===============================================================================

Implementation of the node object.

.. class:: GSNode([pt, type])
	
:param pt: The position of the node.
:param type: The type of the node, GSLINE, GSCURVE or GSOFFCURVE

.. autosummary::
	
	position
	type
	connection

----------
Properties
----------

	'''



def Node__new__(typ, *args, **kwargs):
	return GSNode.alloc().init()
GSNode.__new__ = Node__new__;

def Node__init__(self, pt = None, type = None):
	if pt:
		self.setPosition_(pt)
	if type:
		self.setType_(type)
GSNode.__init__ = Node__init__;

def Node__repr__(self):
	return "<GSNode x=%s y=%s %s %s>" % (self.position.x, self.position.y, nodeConstants[self.type], nodeConstants[self.connection])
GSNode.__repr__ = Node__repr__;

GSNode.position = property(			lambda self: self.valueForKey_("position").pointValue(),
								lambda self, value: self.setPosition_(value))
'''.. attribute:: position
	The position of the node.
	:type: NSPoint'''

GSNode.type = property(			lambda self: self.valueForKey_("type"),
								lambda self, value: self.setType_(value))
'''.. attribute:: type
	The type of the node, GSLINE, GSCURVE or GSOFFCURVE
	:type: int'''
GSNode.connection = property(	lambda self: self.valueForKey_("connection"),
								lambda self, value: self.setConnection_(value))
'''.. attribute:: connection
	The type of the connection, GSSHARP or GSSMOOTH
	:type: int'''










##################################################################################
#
#
#
#           GSGuideLine
#
#
#
##################################################################################


'''

:mod:`GSGuideLine`
===============================================================================

Implementation of the guide line object.

.. class:: GSGuideLine

.. autosummary::
	
	position
	angle
	
----------
Properties
----------


	'''


def GuideLine__new__(typ, *args, **kwargs):
	return GSGuideLine.alloc().init()
GSGuideLine.__new__ = GuideLine__new__;

def GuideLine__init__(self):
	pass
GSGuideLine.__init__ = GuideLine__init__;

def GuideLine__repr__(self):
	return "<GSGuideLine x=%s y=%s angle=%s>" % (self.position.x, self.position.y, self.angle)
GSGuideLine.__repr__ = GuideLine__repr__;

GSGuideLine.position = property(			lambda self: self.valueForKey_("position").pointValue(),
								lambda self, value: self.setPosition_(value))
'''.. attribute:: position
	The position of the node.
	:type: NSPoint'''
GSGuideLine.angle = property(lambda self: self.valueForKey_("angle").floatValue(),
								lambda self, value: self.setAngle_(float(value)))
'''.. attribute:: angle
	Angle
	:type: float'''




##################################################################################
#
#
#
#           GSHint
#
#
#
##################################################################################


'''

:mod:`GSHint`
===============================================================================

Implementation of the hint object.

.. class:: GSHint

.. autosummary::
	
	originNode
	targetNode
	type
	horizontal

----------
Properties
----------

	'''


def Hint__new__(typ, *args, **kwargs):
	return GSHint.alloc().init()
GSHint.__new__ = Hint__new__;

def Hint__init__(self):
	pass
GSHint.__init__ = Hint__init__;

def Hint__repr__(self):
	if self.horizontal:
		direction = "horizontal"
	else:
		direction = "vertical"
	if self.type == BottomGhost or self.type == TopGhost:
		return "<GSHint %s origin=(%s,%s) type=%s>" % (hintConstants[self.type], self.originNode.position.x, self.originNode.position.y, self.type)
	elif self.type == Stem:
		return "<GSHint Stem origin=(%s,%s) target=(%s,%s) %s>" % (self.originNode.position.x, self.originNode.position.y, self.targetNode.position.x, self.targetNode.position.y, direction)
	else:
		return "<GSHint %s %s>" % (hintConstants[self.type], direction)
GSHint.__repr__ = Hint__repr__;

GSHint.originNode = property(	lambda self: self.valueForKey_("originNode"),
								lambda self, value: self.setOriginNode_(value))
'''.. attribute:: originNode
	The the first node this hint is attached to.
	
	:type: :class:`GSNode <GSNode>`
'''
GSHint.targetNode = property(	lambda self: self.valueForKey_("targetNode"),
								lambda self, value: self.setTargetNode_(value))
'''.. attribute:: targetNode
	The the second node this hint is attached to. In case of a ghost hint this value will be empty.
	
	:type: :class:`GSNode <GSNode>`
'''

GSHint.otherNode1 = property(	lambda self: self.valueForKey_("otherNode1"),
								lambda self, value: self.setOtherNode1_(value))
'''.. attribute:: otherNode1
	A third node this hint is attached to. Used for Interpolation or Diagonal hints.
	
	:type: :class:`GSNode <GSNode>`'''
	
GSHint.otherNode2 = property(	lambda self: self.valueForKey_("otherNode1"),
								lambda self, value: self.setOtherNode1_(value))
'''.. attribute:: otherNode2
	A forth node this hint is attached to. Used for Diagonal hints.

	:type: :class:`GSNode <GSNode>`'''

GSHint.type = property(			lambda self: self.valueForKey_("type"),
								lambda self, value: self.setType_(value))
'''.. attribute:: type
	See Constants section at the bottom of the page
	:type: int'''
	
GSHint.horizontal = property(	lambda self: self.valueForKey_("horizontal").boolValue(),
								lambda self, value: self.setHorizontal_(value))
'''.. attribute:: horizontal
	True if hint is horizontal, False if vertical.
	:type: bool'''


##################################################################################
#
#
#
#           GSGlyphsInfo
#
#
#
##################################################################################


'''

:mod:`GSGlyphsInfo`
===============================================================================

Implementation of the GSGlyphsInfo object.

.. class:: GSGlyphsInfo

.. autosummary::

niceNameForName
nameForUnicode

----------
Properties
----------

'''


def GSGlyphsInfo_niceName(self, Name):
	return GSGlyphsInfo.niceGlyphNameForName_(Name)
'''.. function:: niceNameForName(Name)
	
	Converts the Name in a readable name. (converts "uni01D1" in "Ocaron")
	
	:param Name: A glyph name
	:return: The converted Name.
	:rtype: string'''

GSGlyphsInfo.niceNameForName = GSGlyphsInfo_niceName


def GSGlyphsInfo_nameForUnicode(self, Unicode):
	GlyphInfo = GSGlyphsInfo.glyphInfoForUnicode_(Unicode)
	return GlyphInfo.name()

'''.. function:: nameForUnicode(Name)
	
	Converts the Unicode String in a readable name. (converts "01D1" in "Ocaron")
	
	:param Name: A unicode as string representation
	:return: The Name.
	:rtype: string'''

GSGlyphsInfo.nameForUnicode =  GSGlyphsInfo_nameForUnicode


'''

Methods
=======

.. autosummary::

	divideCurve()
	distance()
	addPoints()
	subtractPoints()
	GetOpenFile()
	GetSaveFile()
	Message()
	'''


def divideCurve(P0, P1, P2, P3, t):
	#NSPoint Q0, Q1, Q2, R0, R1;
	Q0x = P0[0] + ((P1[0]-P0[0])*t);
	Q0y = P0[1] + ((P1[1]-P0[1])*t);
	Q1x = P1[0] + ((P2[0]-P1[0])*t);
	Q1y = P1[1] + ((P2[1]-P1[1])*t);
	Q2x = P2[0] + ((P3[0]-P2[0])*t);
	Q2y = P2[1] + ((P3[1]-P2[1])*t);
	R0x = Q0x + ((Q1x-Q0x)*t);
	R0y = Q0y + ((Q1y-Q0y)*t);
	R1x = Q1x + ((Q2x-Q1x)*t);
	R1y = Q1y + ((Q2y-Q1y)*t);
	
	#NSPoint S;
	Sx = R0x + ((R1x-R0x)*t);
	Sy = R0y + ((R1y-R0y)*t);
	#	S: neuer Punkt
	#	R0: Anker 2 zu S
	#	Q0: Anker 1 zu S
	#	R1: Anker  zu N2
	#	Q2: Anker  zu N2
	return (P0, NSMakePoint(Q0x, Q0y), NSMakePoint(R0x, R0y), NSMakePoint(Sx, Sy), NSMakePoint(R1x, R1y), NSMakePoint(Q2x, Q2y), P3)
	#*(q2) = R0;
	#*(q3) = S ;
	#*(r1) = R1;
	#*(r2) = Q2;
	#*(r3) = P3;
'''.. function:: divideCurve(P0, P1, P2, P3, t)
	
	Divides the curve using the De Casteljau's algorithm.
	
	:param P0: The Start point of the Curve (NSPoint)
	:param P1: The first off curve point
	:param P2: The second off curve point
	:param P3: The End point of the Curve
	:param t: The time parameter
	:return: A list of points that represent two curves. (Q0, Q1, Q2, Q3, R1, R2, R3). Note that the "middle" point is only returned once.
	:rtype: list'''
	
	
def distance(P1, P2):
	return math.hypot(P1[0] - P2[0], P1[1] - P2[1])
'''.. function:: distance(P0, P1)
	
	calculates the distance between two NSPoints
	
	:param P0: a NSPoint
	:param P1: another NSPoint
	:return: The distance
	:rtype: float'''
	
	
def addPoints(P1, P2):
	return NSMakePoint(P1[0] + P2[0], P1[1] + P2[1])
'''.. function:: addPoints(P1, P2)
	
	Add the points.

	:param P0: a NSPoint
	:param P1: another NSPoint
	:return: The sum of both points
	:rtype: NSPoint'''
	
	
def subtractPoints(P1, P2):
	return NSMakePoint(P1[0] - P2[0], P1[1] - P2[1])
'''.. function:: subtractPoints(P1, P2)
	
	Subtracts the points.
	
	:param P0: a NSPoint
	:param P1: another NSPoint
	:return: The subtracted point
	:rtype: NSPoint'''
	
def scalePoint(P, scalar):
	return NSMakePoint(P[0] * scalar, P[1] * scalar)
'''.. function:: scalePoint(P, scalar)
	
	Scaled a point.

	:param P: a NSPoint
	:param scalar: The Multiplier
	:return: The multiplied point
	:rtype: NSPoint
'''

def GetSaveFile(message=None, ProposedFileName=None, filetypes=None):
	if filetypes is None:
		filetypes = []
	Panel = NSSavePanel.savePanel().retain()
	if message is not None:
		Panel.setTitle_(message)
	Panel.setCanChooseFiles_(True)
	Panel.setCanChooseDirectories_(False)
	Panel.setAllowedFileTypes_(filetypes)
	if ProposedFileName is not None:
		Panel.setNameFieldStringValue_(ProposedFileName)
	pressedButton = Panel.runModalForTypes_(filetypes)
	if pressedButton == NSOKButton:
		return Panel.filename()
	return None

'''.. function:: GetSaveFile(message=None, ProposedFileName=None, filetypes=None)
	
	Opens a file chooser dialog.
	
	:param message:
	:param filetypes:
	:param ProposedFileName:
	:return: The selected file or None
	:rtype: unicode
'''

def __allValues__(self):
	return self.allValues()
MGOrderedDictionary.items = __allValues__

def __Dict_removeObjectForKey__(self, key):
	if isinstance(key, int):
		if key < 0:
			key += len(self)
			if key < 0:
				raise IndexError("list index out of range")
		self.removeObjectAtIndex_(key)
		return
	self.removeObjectForKey_(key)

MGOrderedDictionary.__delitem__ = __Dict_removeObjectForKey__


#This should be possible but the way pyObjc wrapper works does not allow it.
#http://permalink.gmane.org/gmane.comp.python.pyobjc.devel/5493
#def __Dict__objectForKey__(self, key):
#	if isinstance(key, int):
#		if key < 0:
#			key += len(self)
#			if key < 0:
#				raise IndexError("list index out of range")
#		self.objectAtIndex_(key)
#		return
#	self.objectForKey_(key)
#
#MGOrderedDictionary.__getitem__ = __Dict__objectForKey__


def __Dict__iter__(self):
	Values = self.values()
	if Values is not None:
		for element in Values:
			yield element
MGOrderedDictionary.__iter__ = __Dict__iter__
#MGOrderedDictionary.__len__ = property(lambda self: self.count())

def __Dict__del__(self, key):
	self.removeObjectForKey_(key)
MGOrderedDictionary.__delattr__ = __Dict__del__


def GetFile(message=None, allowsMultipleSelection=False, filetypes=None):
	return GetOpenFile(message, allowsMultipleSelection, filetypes)

def GetOpenFile(message=None, allowsMultipleSelection=False, filetypes=None):
	if filetypes is None:
		filetypes = []
	Panel = NSOpenPanel.openPanel().retain()
	Panel.setCanChooseFiles_(True)
	Panel.setCanChooseDirectories_(False)
	Panel.setAllowsMultipleSelection_(allowsMultipleSelection)
	if message is not None:
		Panel.setTitle_(message)
	if filetypes is not None and len(filetypes) > 0:
		Panel.setAllowedFileTypes_(filetypes)
	pressedButton = Panel.runModalForTypes_(filetypes)
	if pressedButton == NSOKButton:
		if allowsMultipleSelection:
			return Panel.filenames()
		else:
			return Panel.filename()
	return None
'''.. function:: GetOpenFile(message=None, allowsMultipleSelection=False, filetypes=None)
	
	Opens a file chooser dialog.
	
	:param message: A message string.
	:param allowsMultipleSelection: Boolean, True if user can select more than one file
	:param filetypes: list of strings indicating the filetypes, e.g. ["gif", "pdf"]
	
	:return: The selected file or a list of file names or None
	:rtype: unicode or list
'''

def GetFolder(message=None, allowsMultipleSelection=False):
	Panel = NSOpenPanel.openPanel().retain()
	Panel.setCanChooseFiles_(False)
	Panel.setCanChooseDirectories_(True)
	Panel.setAllowsMultipleSelection_(allowsMultipleSelection)
	pressedButton = Panel.runModal()
	if pressedButton == NSOKButton:
		if allowsMultipleSelection:
			return Panel.filenames()
		else:
			return Panel.filename()
	return None

'''.. function:: GetFolder(message=None, allowsMultipleSelection = False)
	
	Opens a folder chooser dialog.
	
	:param message:
	:param allowsMultipleSelection:
	:return: The selected folder or None
	:rtype: unicode
'''

def Message(title, message, OKButton=None):
	Glyphs.showAlert_message_OKButton_(title, message, OKButton)

'''.. function:: Message(title, message, OKButton=None)
	
	Shows a alert panel
	
	:param title:
	:param message:
	:param OKButton:
'''

def newTab(tabText):
	from PyObjCTools.AppHelper import callAfter
	callAfter(Glyphs.currentDocument.windowController().addTabWithString_, tabText)

'''.. function:: newTab(tabText)
	
	Opens a new tab in the current document window
	
	:param tabText: The glyphnames need to be seperated by '/'
'''


'''
Constants
=========

Node types

	GSLINE = 1
		Line node.

	GSCURVE = 35
		Curve node. Make sure that each curve node is preceded by two off-curve nodes.

	GSOFFCURVE = 65
		Off-cuve node

Node connection

	GSSHARP = 0
		Sharp connection.

	GSSMOOTH = 100
		A smooth or tangent node

Hint types

	TOPGHOST = -1
		Top ghost for PS hints
	
	STEM = 0
		Stem for PS hints
	
	BOTTOMGHOST = 1
		Bottom ghost for PS hints
	
	TTANCHOR = 2
		Anchor for TT hints

	TTSTEM = 3
		Stem for TT hints
	
	TTALIGN = 4
		Aling for TT hints

	TTINTERPOLATE = 5
		Interpolation for TT hints

	TTDIAGONAL = 6
		Diagonal for TT hints

	CORNER = 16
		Corner Component

	CAP = 17
		Cap Component
	
Hint Option 
	
	This is only used for TrueType hints.
	
	TTROUND = 0
		Round to grid
		
	TTROUNDUP = 1
		Round up
		
	TTROUNDDOWN = 2
		Round down
		
	TTDONTROUND = 4
		Don’t round at all
		
	TRIPLE = 128
		Indicates a triple hint group. There need to be exactly three horizontal TTStem hints with this setting to take effect.
	
'''
