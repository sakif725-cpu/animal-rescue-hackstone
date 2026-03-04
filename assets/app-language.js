(function () {
	const STORAGE_KEY = 'appLanguage';
	const SUPPORTED_LANGUAGES = new Set(['en', 'hi', 'bn', 'ta', 'te', 'mr', 'gu']);

	const TRANSLATIONS = {
		hi: {
			'Smart Animal Rescue': 'स्मार्ट एनिमल रेस्क्यू',
			'Report. Rescue. Respond.': 'रिपोर्ट करें। बचाव करें। प्रतिक्रिया दें।',
			'Report Injured Animal': 'घायल पशु की रिपोर्ट करें',
			'Track Reports': 'रिपोर्ट ट्रैक करें',
			'Nearby NGOs': 'नज़दीकी NGO',
			'Home': 'होम',
			'Reports': 'रिपोर्ट्स',
			'Profile': 'प्रोफ़ाइल',
			'Creative Login': 'लॉगिन',
			'Animals do have a Soul': 'जानवरों में भी आत्मा होती है',
			'Choose your role to continue': 'जारी रखने के लिए अपनी भूमिका चुनें',
			'User': 'यूज़र',
			'Volunteer': 'वॉलंटियर',
			'Username': 'यूज़रनेम',
			'Password': 'पासवर्ड',
			'Remember Me': 'मुझे याद रखें',
			'Forgot Password': 'पासवर्ड भूल गए',
			'Log In': 'लॉग इन',
			'Volunteer Login': 'वॉलंटियर लॉगिन',
			'Register as Volunteer': 'वॉलंटियर के रूप में रजिस्टर करें',
			'Or continue with': 'या आगे बढ़ें',
			'Volunteer Access': 'वॉलंटियर एक्सेस',
			'Volunteer Portal': 'वॉलंटियर पोर्टल',
			'Enter Volunteer ID and password, or register as a new volunteer.': 'वॉलंटियर आईडी और पासवर्ड दर्ज करें, या नए वॉलंटियर के रूप में रजिस्टर करें।',
			'Volunteer ID': 'वॉलंटियर आईडी',
			'Log In as Volunteer': 'वॉलंटियर के रूप में लॉगिन',
			'Report Injured Animal': 'घायल पशु की रिपोर्ट करें',
			'Tap to add photos': 'फोटो जोड़ने के लिए टैप करें',
			'Location': 'स्थान',
			'Edit on Map': 'मैप पर संपादित करें',
			'Tap "Edit on Map" to load map preview': 'मैप प्रीव्यू लोड करने के लिए "मैप पर संपादित करें" टैप करें',
			'Coordinates: Not detected yet': 'निर्देशांक: अभी पता नहीं चला',
			'Condition': 'स्थिति',
			'Injured': 'घायल',
			'Sick': 'बीमार',
			'Stray/Lost': 'आवारा/खोया',
			'Normal rescue will be solved tomorrow.': 'सामान्य बचाव कल तक पूरा होगा।',
			'⚠️ Submit Emergency Report': '⚠️ आपातकालीन रिपोर्ट सबमिट करें',
			'Track Reports': 'रिपोर्ट ट्रैक करें',
			'Current': 'वर्तमान',
			'Past': 'पिछला',
			'No past reports available': 'कोई पिछली रिपोर्ट उपलब्ध नहीं',
			'No current reports available': 'कोई वर्तमान रिपोर्ट उपलब्ध नहीं',
			'Go back': 'वापस जाएँ',
			'Search by Case ID or keyword': 'केस आईडी या कीवर्ड से खोजें',
			'Volunteer Dashboard': 'वॉलंटियर डैशबोर्ड',
			'Loading dashboard data...': 'डैशबोर्ड डेटा लोड हो रहा है...',
			'Total Reports': 'कुल रिपोर्ट',
			'Resolved Cases': 'सुलझे मामले',
			'Profile Details': 'प्रोफ़ाइल विवरण',
			'Gender': 'लिंग',
			'Age Group': 'आयु समूह',
			'Area': 'क्षेत्र',
			'Save': 'सेव',
			'Close': 'बंद करें',
			'Logout Volunteer': 'वॉलंटियर लॉगआउट',
			'Case Details': 'केस विवरण',
			'Map preview will appear here': 'मैप प्रीव्यू यहाँ दिखेगा',
			'Critical': 'गंभीर',
			'No active case': 'कोई सक्रिय केस नहीं',
			'Reporter': 'रिपोर्टर',
			'Phone unavailable': 'फोन उपलब्ध नहीं',
			'Location unavailable': 'स्थान उपलब्ध नहीं',
			'📞 Call Reporter': '📞 रिपोर्टर को कॉल करें',
			'🚀 Navigate': '🚀 नेविगेट करें',
			'✓ Mark as Completed': '✓ पूर्ण चिह्नित करें',
			'Edit Profile': 'प्रोफ़ाइल संपादित करें',
			'Choose Photo': 'फोटो चुनें',
			'JPG, PNG, WEBP • Max 5MB': 'JPG, PNG, WEBP • अधिकतम 5MB',
			'Name': 'नाम',
			'Phone': 'फोन',
			'Email': 'ईमेल',
			'Address': 'पता',
			'Enter name': 'नाम दर्ज करें',
			'Enter phone': 'फोन दर्ज करें',
			'Enter email': 'ईमेल दर्ज करें',
			'Enter address': 'पता दर्ज करें',
			'Cancel': 'रद्द करें',
			'mins': 'मिनट',
			'hrs': 'घंटे',
			'ago': 'पहले',
			'mins ago': 'मिनट पहले',
			'hrs ago': 'घंटे पहले',
			'Unknown location': 'अज्ञात स्थान',
			'Open': 'खुला',
			'Case ID #': 'केस आईडी #',
			'Case #': 'केस #',
			'Condition:': 'स्थिति:',
			'Updated at': 'अपडेट समय',
			'Reported animal photo': 'रिपोर्ट किए गए पशु का फोटो',
			'Detected location map': 'पहचाना गया स्थान मैप',
			'Selected injured animal photo': 'चुनी गई घायल पशु की फोटो',
			'Photo selected': 'फोटो चुनी गई',
			'Unable to fetch address details.': 'पते का विवरण प्राप्त नहीं हो सका।',
			'Geolocation is not supported by this browser.': 'यह ब्राउज़र जियोलोकेशन को सपोर्ट नहीं करता।',
			'Detecting location...': 'स्थान पता लगाया जा रहा है...',
			'Location detected. Address lookup unavailable right now.': 'स्थान मिला, लेकिन पता अभी उपलब्ध नहीं है।',
			'Unable to detect location. Please allow location access.': 'स्थान पता नहीं चला। कृपया लोकेशन अनुमति दें।',
			'Please add at least one photo before submitting.': 'सबमिट करने से पहले कम से कम एक फोटो जोड़ें।',
			'Location is required to submit. Please enable location access.': 'सबमिट करने के लिए लोकेशन आवश्यक है। कृपया अनुमति दें।',
			'Submitting report...': 'रिपोर्ट सबमिट हो रही है...',
			'Could not submit report right now. Please try again.': 'अभी रिपोर्ट सबमिट नहीं हो सकी। फिर प्रयास करें।',
			'Report submitted successfully. Redirecting to tracking...': 'रिपोर्ट सफलतापूर्वक सबमिट हुई। ट्रैकिंग पर भेजा जा रहा है...',
			'Submitted ✓': 'सबमिट ✓',
			'Injured Animal': 'घायल पशु',
			'Reporter:': 'रिपोर्टर:',
			'Location:': 'स्थान:',
			'View Details': 'विवरण देखें',
			'Navigate': 'नेविगेट करें',
			'Unable to load reports right now': 'अभी रिपोर्ट लोड नहीं हो पा रही हैं',
			'Live data is synced from the server.': 'लाइव डेटा सर्वर से सिंक है।',
			'Welcome': 'स्वागत है',
			'Volunteer ID:': 'वॉलंटियर आईडी:',
			'Member Since:': 'सदस्य कब से:',
			'Not available': 'उपलब्ध नहीं',
			'Unable to load live server data right now.': 'अभी लाइव सर्वर डेटा लोड नहीं हो पाया।',
			'Saving...': 'सेव हो रहा है...',
			'Saved successfully.': 'सफलतापूर्वक सेव हुआ।',
			'Could not save profile details.': 'प्रोफ़ाइल विवरण सेव नहीं हो सके।',
			'Injured animal location': 'घायल पशु का स्थान',
			'Your location': 'आपका स्थान',
			'Injured animal': 'घायल पशु',
			'Map location is unavailable for this case': 'इस केस के लिए मैप लोकेशन उपलब्ध नहीं है',
			'Unable to load case details': 'केस विवरण लोड नहीं हो सके',
			'Case': 'केस',
			'Latest report from server database.': 'सर्वर डेटाबेस से नवीनतम रिपोर्ट।',
			'Could not load server case data.': 'सर्वर केस डेटा लोड नहीं हो सका।',
			'Could not load map right now': 'अभी मैप लोड नहीं हो सका',
			'Reporter contact is not available in current dataset.': 'वर्तमान डेटा में रिपोर्टर संपर्क उपलब्ध नहीं है।',
			'Navigation is unavailable until case details are loaded.': 'केस विवरण लोड होने तक नेविगेशन उपलब्ध नहीं है।',
			'Routing...': 'रूट तैयार हो रहा है...',
			'Destination unavailable': 'गंतव्य उपलब्ध नहीं',
			'Geolocation unavailable': 'जियोलोकेशन उपलब्ध नहीं',
			'Could not draw road route right now.': 'अभी रोड रूट नहीं बनाया जा सका।',
			'Allow location access to create route from your location.': 'अपने स्थान से रूट बनाने के लिए लोकेशन अनुमति दें।',
			'Navigation is unavailable until location and map data are available.': 'लोकेशन और मैप डेटा मिलने तक नेविगेशन उपलब्ध नहीं है।',
			'No active case is available to resolve.': 'सुलझाने के लिए कोई सक्रिय केस उपलब्ध नहीं है।',
			'Updating...': 'अपडेट हो रहा है...',
			'Failed to resolve case': 'केस सुलझाने में विफल',
			'✓ Case Resolved': '✓ केस सुलझा',
			'Case marked as resolved.': 'केस को सुलझा हुआ चिह्नित किया गया।',
			'✓ Mark as Completed': '✓ पूर्ण चिह्नित करें',
			'Could not update case status right now.': 'अभी केस स्थिति अपडेट नहीं हो सकी।',
			'Unable to load profile data from server.': 'सर्वर से प्रोफ़ाइल डेटा लोड नहीं हो सका।',
			'Use JPG, PNG, or WEBP only.': 'केवल JPG, PNG, या WEBP उपयोग करें।',
			'Image is too large. Max size is 5MB.': 'छवि बहुत बड़ी है। अधिकतम आकार 5MB है।',
			'Photo selected. Tap Save to apply.': 'फोटो चुनी गई। लागू करने के लिए सेव दबाएँ।',
			'Failed to save profile': 'प्रोफ़ाइल सेव नहीं हो सकी',
			'Could not save profile right now. Please try again.': 'अभी प्रोफ़ाइल सेव नहीं हो सकी। फिर प्रयास करें।'
		}
	};

	const SHARED_LANGUAGE_KEYS = {
		bn: 'hi',
		ta: 'hi',
		te: 'hi',
		mr: 'hi',
		gu: 'hi'
	};

	function normalizeLanguage(languageCode) {
		const normalized = String(languageCode || '').trim().toLowerCase();
		if (!SUPPORTED_LANGUAGES.has(normalized)) {
			return 'en';
		}
		return normalized;
	}

	function getLanguageMap(languageCode) {
		const normalized = normalizeLanguage(languageCode);
		const mapKey = SHARED_LANGUAGE_KEYS[normalized] || normalized;
		return TRANSLATIONS[mapKey] || {};
	}

	function getCurrentLanguage() {
		try {
			return normalizeLanguage(window.localStorage.getItem(STORAGE_KEY) || 'en');
		} catch (error) {
			return 'en';
		}
	}

	function setCurrentLanguage(languageCode) {
		const normalized = normalizeLanguage(languageCode);
		try {
			window.localStorage.setItem(STORAGE_KEY, normalized);
		} catch (error) {
			/* no-op */
		}
		document.documentElement.lang = normalized;
		return normalized;
	}

	function translateString(sourceText, languageCode) {
		const source = String(sourceText || '');
		const trimmed = source.trim();
		if (!trimmed) {
			return source;
		}

		const dictionary = getLanguageMap(languageCode || getCurrentLanguage());
		const translated = dictionary[trimmed];
		if (!translated) {
			return source;
		}

		if (source === trimmed) {
			return translated;
		}

		return source.replace(trimmed, translated);
	}

	function translateAttributes(rootElement, languageCode) {
		const selectors = [
			'input[placeholder]',
			'textarea[placeholder]',
			'[aria-label]',
			'[title]'
		];

		const nodes = rootElement.querySelectorAll(selectors.join(','));
		nodes.forEach(function (node) {
			if (node.hasAttribute('placeholder')) {
				node.setAttribute('placeholder', translateString(node.getAttribute('placeholder'), languageCode));
			}
			if (node.hasAttribute('aria-label')) {
				node.setAttribute('aria-label', translateString(node.getAttribute('aria-label'), languageCode));
			}
			if (node.hasAttribute('title')) {
				node.setAttribute('title', translateString(node.getAttribute('title'), languageCode));
			}
		});
	}

	function translateTextNodes(rootElement, languageCode) {
		const walker = document.createTreeWalker(rootElement, NodeFilter.SHOW_TEXT, {
			acceptNode: function (node) {
				if (!node || !node.nodeValue || !node.nodeValue.trim()) {
					return NodeFilter.FILTER_REJECT;
				}
				const parent = node.parentElement;
				if (!parent) {
					return NodeFilter.FILTER_REJECT;
				}
				const tagName = parent.tagName;
				if (tagName === 'SCRIPT' || tagName === 'STYLE' || tagName === 'NOSCRIPT') {
					return NodeFilter.FILTER_REJECT;
				}
				return NodeFilter.FILTER_ACCEPT;
			}
		});

		const nodes = [];
		while (walker.nextNode()) {
			nodes.push(walker.currentNode);
		}

		nodes.forEach(function (node) {
			node.nodeValue = translateString(node.nodeValue, languageCode);
		});
	}

	function applyTranslations(rootElement) {
		const root = rootElement || document.body;
		if (!root) {
			return;
		}

		const languageCode = getCurrentLanguage();
		document.documentElement.lang = languageCode;
		translateTextNodes(root, languageCode);
		translateAttributes(root, languageCode);
	}

	function init() {
		setCurrentLanguage(getCurrentLanguage());
		applyTranslations(document.body);
	}

	window.AppLanguage = {
		storageKey: STORAGE_KEY,
		init: init,
		applyTranslations: applyTranslations,
		t: function (sourceText) {
			return translateString(sourceText, getCurrentLanguage());
		},
		getLanguage: getCurrentLanguage,
		setLanguage: function (languageCode) {
			setCurrentLanguage(languageCode);
			applyTranslations(document.body);
		}
	};

	if (document.readyState === 'loading') {
		document.addEventListener('DOMContentLoaded', init);
	} else {
		init();
	}
})();
