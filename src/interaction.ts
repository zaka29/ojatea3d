import { useEffect, useState } from 'react'

export function useReducedMotion() {
  const [reduced, setReduced] = useState(() => window.matchMedia('(prefers-reduced-motion: reduce)').matches)
  useEffect(() => {
    const query = window.matchMedia('(prefers-reduced-motion: reduce)')
    const update = () => setReduced(query.matches)
    query.addEventListener('change', update)
    return () => query.removeEventListener('change', update)
  }, [])
  return reduced
}

// Scene shortcuts must leave focused menus and buttons to their native keyboard behavior.
export function isSceneShortcut(event: KeyboardEvent) {
  const target = event.target
  return !event.repeat && !event.altKey && !event.ctrlKey && !event.metaKey &&
    !(target instanceof HTMLElement && target.closest('button, input, select, textarea, [contenteditable="true"]'))
}
