/* ***** BEGIN LICENSE BLOCK *****
 *
 * Copyright (C) 2009, 2010, 2011  Stéphane Sire
 *
 * This file is part of the Adaptable XML Editing Library (AXEL), version 1.1.2-beta 
 *
 * Adaptable XML Editing Library (AXEL) is free software ; you can redistribute it 
 * and/or modify it under the terms of the GNU Lesser General Public License (the "LGPL")
 * as published by the Free Software Foundation ; either
 * version 2.1 of the License, or (at your option) any later version.
 *
 * The library is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY ; 
 * without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR 
 * PURPOSE. See the GNU Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License along with this library ; 
 * if not, write to the Free Software Foundation, Inc., 59 Temple Place, Suite 330, 
 * Boston, MA 02111-1307 USA.
 *
 * Web site : http://media.epfl.ch/Templates/
 * 
 * Author(s) : Stephane Sire, Antoine Yersin
 * 
 * ***** END LICENSE BLOCK ***** */

// open issue: should we create one keyboard instance per document or not ?

/**
 * Centralizes keyboard input among several input devices (e.g. each <input> or <textarea>)
 * This is useful in particular to factorize the tab management code
 * 
 * @class Keyboard
 */
xtiger.editor.Keyboard = function () {
	this.tabGroupManager = false;
	this.currentDevice = false;   
	this.allowRC = false;
}

// FIXME: dans register memoriser tous les abonnements pour les desabonner sur une method (reset)
// à appeler quand on change de document // frame (?)
xtiger.editor.Keyboard.prototype = {
		
		/**
		 * 
		 * @param t
		 * @return
		 */
	setTabGroupManager : function (t) {
		this.tabGroupManager = t;
	},
	
	/**
	 * Allows a device to register to keyboard events on its handle.
	 * 
	 * @param {Device}
	 *            aDevice
	 * @param {DOMElement|DOMDocument}
	 *            aAltHandle Optional. A handle listening to DOM events. If not
	 *            submitted, the device's default handle (device.getHandle()) is
	 *            used.
	 * @return {[function]} Handler's references to unregister
	 */
	register : function (aDevice, aAltHandle) {
		
		var _handle = aAltHandle ? aAltHandle : aDevice.getHandle();
		
		// closure variables
		var _this = this;
		var _device = aDevice;
		
		var _handlers = {
				keydown: function (ev) { _this.handleKeyDown(ev, _device) },
				keyup: function (ev) { _this.handleKeyUp(ev, _device) }
		}
		xtdom.addEventListener(_handle, 'keydown', _handlers.keydown, false);
		xtdom.addEventListener(_handle, 'keyup', _handlers.keyup, false);
		return _handlers;
	},
	
	/**
	 * 
	 * @param device
	 * @param handlers
	 * @return
	 */
	unregister : function (aDevice, handlers, aAltHandle) {			
		var _handle = aAltHandle ? aAltHandle : aDevice.getHandle();
		xtdom.removeEventListener(_handle, 'keydown', handlers.keydown, false);
		xtdom.removeEventListener(_handle, 'keyup', handlers.keyup, false);
	},
	
	// Esc does not trigger keyPress on Safari, hence we need to intercept it with keyDown
	handleKeyDown : function (ev, device) {
		if (device.isEditing()) {
			if (this.tabGroupManager) {
				this.tabGroupManager.filterKeyDown(ev);
			}                              
			// On FF ctrlKey+ RC sends an event but the line break is not added to the textarea hence I have selected shiftKey                       
			var validate = (this.allowRC && (ev.keyCode == 13) && (! ev.shiftKey)) || ((!this.allowRC) && (ev.keyCode == 13));
			if (validate) {
				device.stopEditing(false);
			} else if (ev.keyCode	== 27) {
				device.cancelEditing ();
			}			
			device.doKeyDown (ev);			
		}	
	},
	handleKeyUp : function (ev, device) {
		if (device.isEditing()) {
			if (this.tabGroupManager && this.tabGroupManager.filterKeyPress(ev)) {      
				xtdom.preventDefault(ev);
				xtdom.stopPropagation(ev);
			} else {
				device.doKeyUp (ev);
			}
		}
	},
	grab : function (device, editor) {
		if (this.tabGroupManager) {
			this.tabGroupManager.startEditingSession (editor);
			// window.console.log('TabGroupManager start editing ' + editor);
		}
	},
	release : function (device, editor) {
		if (this.tabGroupManager) {
			this.tabGroupManager.stopEditingSession ();
			// window.console.log('TabGroupManager stop editing');
		}
	},
	enableRC : function () {  
		this.allowRC = true;     
	}, 
	disableRC : function () {
		this.allowRC = false;
	}
}
