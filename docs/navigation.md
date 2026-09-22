# Navigation and page contents

The shared header is the site-level navigation: Worlds, Scenario, Fleet, Characters, Materials. The desktop sidebar contains only the current page's contents and an optional contextual parent link. Source dialogue and art-brief links remain in the homepage Materials directory, rather than repeating in every sidebar.

On mobile/tablet (960px or narrower), the header's links move into the same drawer as page contents. Opening the drawer traps keyboard focus and makes the background inert; Escape, backdrop and the close button dismiss it. Closing restores focus. The drawer is hidden from keyboard navigation while closed.

Native `details` groups collapse long lists. Their state is retained for the browser session, per page. Direct hash links reopen the relevant group. Active sections highlight their parent group without continually forcing groups open during scrolling. The existing scenario chapter tree and its expand/collapse controls are retained.

`scripts/navigation.py` owns the static shell. All four content builders call it after generating pages. It can also run independently with Python and BeautifulSoup. `assets/navigation.css` is loaded last to override older page-specific shell styles; interaction lives in `assets/solar.js`.

The September navigation pass preserved the main content, anchor IDs and images on all 25 pages, and removed the temporary chat-message popup after VS Code recovered.
