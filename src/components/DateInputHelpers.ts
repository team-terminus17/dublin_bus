export function toISOString(date: Date): string {

    // The javascript month is zero based!
    return date.getUTCFullYear()
        + "-" + (date.getUTCMonth() + 1).toString().padStart(2, "0")
        + "-" + date.getUTCDate().toString().padStart(2, "0")

}

export function parseISOString(input: string, name:string|null): Date|null {

    if (!input)
        return null

    // Standard ISO format - YYYY-MM-DD
    const pattern = /(\d\d\d\d)-(\d\d)-(\d\d)/i
    const match = input.toString().match(pattern)
    if (!match) {
         if (name)
                throw `Expected ${name} in ISO format: YYYY-MM-DD. Found '${input}' instead.`
            else
                return null
    }

    const year = parseInt(match[1])
    // The javascript month is zero based!
    const month = parseInt(match[2]) - 1
    const day = parseInt(match[3])

    return new Date(Date.UTC(year, month, day))

}

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export function parseDateRange(startText: string, endText: string, name: string) {

  let startDate = parseISOString(startText, `${name} start-date`)
  let endDate = parseISOString(endText, `${name} DateInputCalendar end-date`)

  if (!startDate) startDate = new Date(Date.now())
  if (!endDate) {
    endDate = new Date(Date.now())
    endDate.setDate(endDate.getDate() + 14)
  }

  if (endDate < startDate)
    endDate = startDate

  return {
    start: startDate,
    end: endDate
  }

}