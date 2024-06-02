import { FC, useEffect, useState } from "react"

const Main: FC = () => {
    const [loading, setLoading] = useState<boolean>(true)
    const [reading, setReading] = useState<boolean>(false)
    const [cards, serCards] = useState<string[]>([])


    const Card: FC<{ card: string }> = ({ card }) => {
        return <img
            src={`https://optcgplayer.com/images/EN/${card}.png`}
            alt={card}
            // className="dark:invert"
            width={"30px"}
        />
    }

    const getCards = async () => {
        console.log("#### fetching cards")
        const res = await fetch("/api/cards")
        console.log("#### res", res)
        const json = (await res.json())
        console.log("#### json ", json)
        setLoading(false)

        const { cards: cardsResponse, reading: readingRes } = json
        if (cardsResponse.length !== cards.length) {
            serCards(cards.map(card => card.toUpperCase()))
        }
        if (readingRes !== reading) {
            setReading(readingRes) }

            if (reading) {
                await new Promise((res) => { setTimeout(() => res(true), 1000) })
                getCards()
            }
        }



        useEffect(() => {
            getCards()
        }, [])

        return <div className="z-10 w-full max-w-5xl items-center justify-between font-mono text-sm lg:flex">
            {cards.map(card => <Card card={card} key={card} />)}
            {loading ? "loading...." : <button
                onClick={async () => {
                    await fetch(reading ? "/api/cards/stop" : "/api/cards/start")
                    setReading(!reading)
                    if (reading) { getCards() }
                }
                } >
                {reading ? "Stop" : "Start"}
            </button>}
        </div>

    }

    export default Main