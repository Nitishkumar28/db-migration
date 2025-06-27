export const handle_datetime = (date_string) => {
    const sanitized = date_string.replace(/\.\d{3,}$/, (match) => match.slice(0, 4));
    const dateObj = new Date(sanitized);
    const readable = dateObj.toLocaleString(); // e.g., "6/22/2025, 1:08:23 PM"
    return readable;
}
