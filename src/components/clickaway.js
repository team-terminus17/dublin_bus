export function onClickaway(target, callback) {
  const listener = (event) => {
    const away = !target.contains(event.target);
    if (away) callback();
  }

  document.addEventListener("click", listener);
  return listener;
}

export function offClickaway(handle) {
  document.removeEventListener("click", handle);
}