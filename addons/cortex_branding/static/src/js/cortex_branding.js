/** @odoo-module **/
/**
 * CortexONE Branding — JS patches
 * License: LGPL-3 — https://www.gnu.org/licenses/lgpl-3.0.html
 * Copyright (C) 2024 Cortex AI Technologies
 */

import { patch } from "@web/core/utils/patch";
import { WebClient } from "@web/webclient/webclient";

// Override the browser tab title to show CortexONE instead of Odoo
patch(WebClient.prototype, {
    setup() {
        super.setup(...arguments);
        // Replace title after mount
        document.title = document.title.replace(/\bodoo\b/gi, 'CortexONE');
    },
});

// MutationObserver: continuously replace any "Odoo" text that slips through
// in DOM text nodes (e.g., from translations not yet overridden)
const REPLACEMENTS = [
    { pattern: /\bOdoo\b/g,               replacement: 'CortexONE' },
    { pattern: /\bPowered by Odoo\b/gi,   replacement: 'Powered by CortexONE' },
    { pattern: /\bodoo\.com\b/gi,         replacement: 'cortexaitechnologies.com' },
];

function patchTextNode(node) {
    if (node.nodeType !== Node.TEXT_NODE) return;
    let val = node.nodeValue;
    REPLACEMENTS.forEach(({ pattern, replacement }) => {
        val = val.replace(pattern, replacement);
    });
    if (val !== node.nodeValue) node.nodeValue = val;
}

function walkAndPatch(root) {
    const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, null);
    let node;
    while ((node = walker.nextNode())) patchTextNode(node);
}

const observer = new MutationObserver((mutations) => {
    for (const m of mutations) {
        if (m.type === 'characterData') {
            patchTextNode(m.target);
        } else {
            m.addedNodes.forEach((n) => walkAndPatch(n));
        }
    }
});

document.addEventListener('DOMContentLoaded', () => {
    walkAndPatch(document.body);
    observer.observe(document.body, {
        childList: true,
        subtree: true,
        characterData: true,
    });
});
