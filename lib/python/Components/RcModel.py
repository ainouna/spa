from __future__ import print_function
from os.path import isfile, join as path_join

from boxbranding import getBoxType, getMachineBrand, getMachineBuild, getBrandOEM

from Tools.Directories import SCOPE_SKIN, pathExists, resolveFilename
from Tools.StbHardware import getFPVersion


class RcModel:
	def __init__(self):
		self.boxTypes = {
			"9900lx": "protek1",
			"9910lx": "protek2",
			"9911lx": "protek2",
			"9920lx": "protek2",
			"AZModel_elite": "azboxelite",
			"AZModel_me": "azboxme",
			"AZModel_minime": "azboxme",
			"AZModel_premium": "azboxhd",
			"AZModel_premium+": "azboxhd",
			"AZModel_ultra": "azboxelite",
			"BrandOEM_fulan": "fulan",
			"MachineBrand_FEGASUS": "ini6",
			"MachineBrand_SPACE": "ini6",
			"MachineBrand_XSARIUS": "fusionhd",
			"MachineBrand_ini3": "ini3",
			"MachineBuild_cube": "cube",
			"MachineBuild_e3hd": "e3hd",
			"MachineBuild_ebox": "ebox5000",
			"MachineBuild_odinm7": "odinm7",
			"MachineBuild_odinm9": "odinm9",
			"MachineBuild_xp1000": "xp1000",
			"alien5": "amiko3",
			"alphatriple": "sab1",
			"anadol4k": "anadol1",
			"anadol4kcombo": "anadol1",
			"anadol4kv2": "anadol1",
			"anadolmulti": "anadol2",
			"anadolmultitwin": "anadol2",
			"anadolmultiboxse": "anadol2",
			"anadolprohd5": "anadol3",
			"ip8": "anadol4",
			"arivacombo": "ariva",
			"arivatwin": "ariva",
			"atemio5x00": "ini4",
			"atemio6000": "ini4",
			"atemio6100": "ini4",
			"atemio6200": "ini4",
			"atemionemesis": "ini4",
			"ax51": "ax51",
			"ax60": "ax51",
			"ax61": "ax4",
			"axmulticombo": "ax5",
			"axmultitwin": "ax5",
			"axmultiboxse": "ax5",
			"axashis4kcombo": "axas1",
			"axashis4kcomboplus": "axas1",
			"axashisc4k": "axas2",
			"axas4kcombo": "axas2",
			"axas4ktwin": "axas2",
			"axashistwin": "axas3",
			"axashistwinplus": "axas4",
			"axodin": "odinm6",
			"axodinc": "odinm6",
			"axultra": "ax51",
			"bcm7251s": "hd1100",
			"bcm7252": "hd2400",
			"bcm7358": "xcore2",
			"beyonwizt2": "ini7",
			"beyonwizt3": "ini5",
			"beyonwizt4": "ini7",
			"beyonwizu4": "beyonwiz1",
			"beyonwizv2": "beyonwiz2",
			"bre2ze": "wwio1",
			"bre2ze4k": "wwio1",
			"bre2zet2c": "wwio1",
			"clap4k": "cc1",
			"dinobot4k": "dinobot1",
			"dinobot4kelite": "dinobot1",
			"dinobot4kl": "dinobot1",
			"dinobot4kmini": "dinobot1",
			"dinobot4kplus": "dinobot1",
			"dinobot4kpro": "dinobot1",
			"dinobot4kse": "dinobot1",
			"dinoboth265": "dinobot1",
			"dinobotu55": "dinobot1",
			"dinobot4ktwin": "dinobot2",
			"dm500hd": "dmm1",
			"dm500hdv2": "dmm2",
			"dm520": "dmm2",
			"dm525": "dmm2",
			"dm7020hd": "dmm2",
			"dm7020hdv2": "dmm2",
			"dm7080": "dmm2",
			"dm800": "dmm1",
			"dm8000": "dmm0",
			"dm800se": "dmm1",
			"dm800sev2": "dmm2",
			"dm820": "dmm2",
			"dm900": "dmm2",
			"dm920": "dmm2",
			"dreamone": "dmm3",
			"dreamtwo": "dmm3",
			"e4hd": "e4hd",
			"e4hdcombo": "e4hdcombo",
			"e4hdhybrid": "e4hd",
			"e4hdultra": "e4hdcombo",
			"enfinity": "evo1",
			"enibox": "hdbox",
			"et10000": "et8000",
			"et4x00": "et4x00",
			"et5000": "et6x00",
			"et5x00": "et6x00",
			"et6000": "et6x00",
			"et6500": "et6500",
			"et6x00": "et6x00",
			"et7000": "et7x00",
			"et7100": "et7x00",
			"et7500": "et7x00",
			"et7x00mini": "et7x00mini",
			"et8000": "et8000",
			"et8500": "et8000",
			"et8500s": "et8000",
			"et9000": "et9x00",
			"et9200": "et9x00",
			"et9500": "et9500",
			"et9x00": "et9x00",
			"evomini": "evo5",
			"evominiplus": "evo5",
			"evoslim": "evo8",
			"evoslimse": "evo8",
			"evoslimt2c": "evo8",
			"ferguson4k": "dinobot1",
			"force1": "iqon2",
			"force1plus": "iqon2",
			"force2": "iqon1",
			"force2nano": "iqon1",
			"force2plus": "iqon1",
			"force2plushv": "iqon1",
			"force2se": "iqon1",
			"force3uhd": "iqon3",
			"force3uhdplus": "iqon3",
			"force4": "iqon1",
			"formuler1": "formuler1",
			"formuler1tc": "formuler1",
			"formuler3": "formuler1",
			"formuler3ip": "formuler1",
			"formuler4": "formuler1",
			"formuler4ip": "formuler1",
			"formuler4turbo": "formuler1",
			"galaxy4k": "revo",
			"gb800se": "gb0",
			"gb800seplus": "gb0",
			"gb800solo": "gb0",
			"gb800ue": "gb0",
			"gb800ueplus": "gb0",
			"gbip4k": "gb4",
			"gbipbox": "gb0",
			"gbquad": "gb0",
			"gbquad4k": "gb3",
			"gbquadplus": "gb1",
			"gbtrio4k": "gb4",
			"gbtrio4kpro": "gb5",
			"gbue4k": "gb4",
			"gbultrase": "gb0",
			"gbultraue": "gb0",
			"gbultraueh": "gb2",
			"gbx1": "gb0",
			"gbx2": "gb2",
			"gbx3": "gb0",
			"gbx34k": "gb3",
			"gbx3h": "gb2",
			"gi11000": "et7x00mini",
			"hitube4k": "hitube1",
			"hitube4kpro": "hitube2",
			"hitube4kplus": "hitube2",
			"hs7429": "hs7429",
			"iqonios100hd": "iqon1",
			"iqonios200hd": "iqon1",
			"iqonios300hd": "iqon1",
			"iqonios300hdv2": "iqon1",
			"ixussone": "ixussone",
			"ixusszero": "ixusszero",
			"iziboxecohd": "izibox2",
			"iziboxone4k": "izibox1",
			"iziboxelite4k": "izibox2",
			"iziboxone4kplus": "izibox2",
			"iziboxx3": "izibox1",
			"jdhdduo": "jd1",
			"lunix": "qviart1",
			"lunix34k": "qviart1",
			"lunix4k": "qviart3",
			"lunixco": "qviart4",
			"dual": "qviart5",
			"og2ott4k": "qviart6",
			"mago": "relook",
			"marvel1": "visionnet",
			"maxytecmulti": "maxytec1",
			"maxytecmultise": "maxytec1",
			"mbmicro": "miraclebox",
			"mbmicrov2": "miraclebox",
			"mbtwinplus": "miraclebox",
			"mediaart200hd": "iqon1",
			"mediabox": "mediabox",
			"mediabox4k": "mediabox4k",
			"megaforce1plus": "megasat2",
			"megaforce2": "megasat1",
			"mutant11": "hd1100",
			"mutant1100": "hd1100",
			"mutant1200": "hd1100",
			"mutant1265": "hd1100",
			"mutant1500": "hd1100",
			"mutant2400": "hd2400",
			"mutant500c": "hd1100",
			"mutant51": "hd1100",
			"mutant530c": "hd530c",
			"mutant60": "hd60",
			"mutant61": "hd60",
			"mutant66se": "hd66se",
			"novaler4k": "novaler1",
			"novaler4kse": "novaler1",
			"novaler4kpro": "novaler1",
			"novacombo": "evo7",
			"novaip": "evo6",
			"novatwin": "evo7",
			"odin2hybrid": "ax1",
			"odinm6": "odinm6",
			"odinplus": "ax1",
			"odroidc2": "hardkernel",
			"opticumtt": "ini8",
			"optimussos": "optimuss1",
			"optimussos1": "optimuss1",
			"optimussos1plus": "optimuss1",
			"optimussos2": "optimuss1",
			"optimussos2plus": "optimuss1",
			"optimussos3plus": "optimuss2",
			"osmega": "xcore3",
			"osmini": "xcore3",
			"osmini4k": "edision3",
			"osminiplus": "xcore3",
			"osmio4k": "edision3",
			"osmio4kplus": "edision3",
			"osnino": "edision1",
			"osninoplus": "edision1",
			"osninopro": "edision2",
			"protek4k": "protek2",
			"protek4kx1": "protek3",
			"protek4kx2": "protek3",
			"pulse4k": "abcom",
			"pulse4kmini": "abcom",
			"quadbox2400": "hd2400",
			"revo4k": "revo",
			"roxxs200hd": "iqon1",
			"sezam1000hd": "ini2",
			"sezam5000hd": "ini2",
			"sezammarvel": "ini4",
			"sf108": "sf108",
			"sf128": "sf3038",
			"sf138": "sf3038",
			"sf208": "sf2x8",
			"sf228": "sf2x8",
			"sf238": "sf2x8",
			"sf3038": "sf3038",
			"sf4008": "sf3038",
			"sf5008": "sf5008",
			"sf8008": "octagon1",
			"sf8008m": "sf8008",
			"sf8008s": "octagon1",
			"sf8008t": "octagon1",
			"sf8008opt": "sf8008",
			"sfx6008": "octagon3",
			"sfx6018": "octagon3",
			"sx88v2": "octagon3",
			"sx888": "octagon3",
			"sx988": "octagon2",
			"ip8": "octagon2",
			"sf98": "sf98",
			"singleboxlcd": "red2",
			"sogno8800hd": "sogno",
			"spycat": "xcore1",
			"spycat4k": "xcore1",
			"spycat4kcombo": "xcore1",
			"spycat4kmini": "xcore1",
			"spycatmini": "xcore1",
			"spycatminiplus": "xcore1",
			"spycatminiv2": "spycat1",
			"starsatlx": "odinm6",
			"t2cable": "evo4",
			"tiviaraplus": "tiviar1",
			# "tiviaraplus": "tiviar2",
			"tiviarmin": "tiviar1",
			"tm2t": "tm1",
			"tm4ksuper": "tm6",
			"tmnano": "tm2",
			"tmnano2super": "tm2",
			"tmnano2t": "tm2",
			"tmnano3t": "tm2",
			"tmnanom3": "tm5",
			"tmnanose": "tm3",
			"tmnanosecombo": "tm3",
			"tmnanosem2": "tm4",
			"tmnanosem2plus": "tm4",
			"tmnanoseplus": "tm4",
			"tmsingle": "tm2",
			"tmtwin": "tm1",
			"tmtwin4k": "tm6",
			"triplex": "triplex",
			"turing": "turing",
			"twinboxlcd": "red1",
			"twinboxlcdci": "red2",
			"twinboxlcdci5": "red2",
			"tyrant": "tyrant",
			"ultrabox": "triplex",
			"ultrav8plus": "maxytec1",
			"uniboxhd1": "ini0" if str(getFPVersion()).startswith("1") else "ini2",
			"uniboxhd2": "ini1",
			"uniboxhd3": "ini1",
			"uniboxhde": "uniboxhde",
			"ustym4kpro": "uclan1",
			"ustym4kprosingle": "uclan1",
			"ustym4kprotwin": "uclan1",
			"ustym4kottpremium": "uclan2",
			"ustym4ks2ottx": "uclan3",
			"valalinux": "vala",
			"vimastec1000": "hd1100",
			"vimastec1500": "hd1100",
			"viper4k": "amiko4",
			"viper4k51": "amiko5",
			"viper4kv20": "amiko6",
			"viper4kv30": "amiko6",
			"viper4kv40": "amiko6",
			"vipercombo": "amiko2",
			"vipercombohdd": "amiko1",
			"viperslim": "amiko2",
			"vipert2c": "amiko2",
			"vipersingle": "amiko6",
			"vipertwin": "amiko6",
			"vizyonvita": "hd1100",
			"vp7358ci": "xcore2",
			"vuduo": "vu",
			"vuduo2": "vu3",
			"vuduo4k": "vu4",
			"vuduo4kse": "vu4",
			"vusolo": "vu",
			"vusolo2": "vu",
			"vusolo4k": "vu",
			"vusolose": "vu",
			"vuultimo": "vu2",
			"vuultimo4k": "vu",
			"vuuno": "vu",
			"vuuno4k": "vu",
			"vuuno4kse": "vu4",
			"vuzero": "vu",
			"vuzero4k": "vu4",
			"wetekhub": "wetek3",
			"wetekplay": "wetek",
			"wetekplay2": "wetek2",
			"worldvisionf1": "iqon2",
			"worldvisionf1plus": "iqon2",
			"x1plus": "evo3",
			"x2plus": "evo2",
			"xcombo": "evo3",
			"xpeedlx": "ini4",
			"xpeedlx1": "ini4",
			"xpeedlx2": "ini4",
			"xpeedlx3": "ini4",
			"xpeedlxcc": "gi1",
			"xpeedlxcs2": "gi1",
			"xpeedlxpro": "ini6",
			"zgemmah10": "zgemma3",
			"zgemmah10se": "zgemma3",
			"zgemmah102h": "zgemma7",
			"zgemmah102s": "zgemma7",
			"zgemmah10combo": "zgemma7",
			"zgemmah11": "zgemma3",
			"zgemmah11s": "zgemma3",
			"zgemmah112h": "zgemma3",
			"zgemmah2h": "zgemma3",
			"zgemmah2s": "zgemma3",
			"zgemmah2splus": "zgemma3",
			"zgemmah32tc": "zgemma3",
			"zgemmah3ac": "zgemma3",
			"zgemmah4": "zgemma3",
			"zgemmah5": "zgemma3",
			"zgemmah52s": "zgemma3",
			"zgemmah52splus": "zgemma3",
			"zgemmah52tc": "zgemma3",
			"zgemmah5ac": "zgemma3",
			"zgemmah6": "zgemma3",
			"zgemmah7": "zgemma3",
			"zgemmah7c": "zgemma3",
			"zgemmah7s": "zgemma3",
			"zgemmah82h": "zgemma3",
			"zgemmah92h": "zgemma3",
			"zgemmah92s": "zgemma3",
			"zgemmah9combo": "zgemma3",
			"zgemmah9combose": "zgemma3",
			"zgemmah9s": "zgemma6",
			"zgemmah9se": "zgemma3",
			"zgemmah92hse": "zgemma3",
			"zgemmah9sse": "zgemma3",
			"zgemmah9splus": "zgemma6",
			"zgemmah9t": "zgemma6",
			"zgemmah9twin": "zgemma3",
			"zgemmah9twinse": "zgemma3",
			"zgemmahs": "zgemma3",
			"zgemmahzeros": "zgemma3",
			"zgemmai55": "zgemma5",
			"zgemmai55se": "zgemma3",
			"zgemmai55plus": "zgemma3",
			"zgemmas2s": "zgemma1",
			"zgemmash1": "zgemma1",
			"zgemmash2": "zgemma2",
			"zgemmaslc": "zgemma2",
			"zgemmass": "zgemma2"
		}
		self.machineBrands = {
			"FEGASUS": "MachineBrand_FEGASUS",
			"SPACE": "MachineBrand_SPACE",
			"XSARIUS": "MachineBrand_XSARIUS"
		}
		self.machineBuilds = {
			"cube": "MachineBuild_cube",
			"e3hd": "MachineBuild_e3hd",
			"odinm7": "MachineBuild_odinm7",
			"odinm9": "MachineBuild_odinm9",
			"xp1000": "MachineBuild_xp1000"
		}

	def rcIsDefault(self):
		# Default RC can only happen with DMM type remote controls.
		return True if self.getRcFolder() == 'dmm0' else False

	def process(self, line):
		if line.lower().startswith('config.usage.rc_model='):
			parts = line.split('=')
			folder = parts[-1].rstrip()
			if isfile('/usr/share/enigma2/rc_models/rc.png') and isfile('/usr/share/enigma2/rc_models/rcpositions.xml') and isfile('/usr/share/enigma2/rc_models/remote.html'):
				return folder
		return None

	# Don't try to be clever and use E2 functions here ...
	def readE2Settings(self):
		try:
			with open('/etc/enigma2/settings') as config:
				for line in config:
					ret = self.process(line)
					if ret is not None:
						return ret
		except IOError as e:
			print("[RcModel] IOError: '/etc/enigma2/settings' cannot be opened")
		return None

	def getRcFolder(self, GetDefault=False):
		if not GetDefault:
			ret = self.readE2Settings()
			if ret is not None:
				return ret

		boxType = getBoxType()
		if pathExists("/proc/stb/info/azmodel"):
			try:
				with open("/proc/stb/info/model", "r") as fd:
					model = f.readline().strip()
					boxType = {
						"elite": "AZModel_elite",
						"me": "AZModel_me",
						"minime": "AZModel_minime",
						"premium": "AZModel_premium",
						"premium+": "AZModel_premium+",
						"ultra": "AZModel_ultra"
					}.get(model, boxType)
			except (IOError, OSError):
				pass
		elif getMachineBrand() == "Miraclebox" and boxType not in ("mbmicro", "mbmicrov2", "mbtwinplus"):
			boxType = "MachineBrand_ini3"
		elif getBrandOEM() == "fulan":
			boxType = "BrandOEM_fulan"
		elif getMachineBuild().startswith("ebox"):
			boxType = "MachineBuild_ebox"
		boxType = self.machineBuilds.get(getMachineBuild(), boxType)
		return self.boxTypes.get(boxType, "dmm0")

	def getRcImg(self):
		return resolveFilename(SCOPE_SKIN, path_join("rc_models", self.getRcFolder(), "rc.png"))

	def getRcPositions(self):
		return resolveFilename(SCOPE_SKIN, path_join("rc_models", self.getRcFolder(), "rcpositions.xml"))

	def getRcLocation(self):
		return resolveFilename(SCOPE_SKIN, path_join("rc_models", self.getRcFolder(), ""))


rc_model = RcModel()