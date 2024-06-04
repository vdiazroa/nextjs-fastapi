import { FC, useEffect, useState } from "react"
import cardsJSON from "../cards.json"

const Main: FC = () => {
    const [loading, setLoading] = useState<boolean>(true)
    const [cards, serCards] = useState<string[]>([])

    const Card: FC<{ card: string }> = ({ card }) => {
        return <img
                src={`https://optcgplayer.com/images/EN/${(cardsJSON as Record<string, string>)[card]}.png`}
                alt={card}
                width={"150px"}
                height={"200px"}
		style={{ margin: "1px" }}
        />
    }

    const getCards = async () => {
        console.log("#### fetching cards")
        const res = await fetch("/api/cards")
        console.log("#### res", res)
        const json = (await res.json())
        const { cards: cardsResponse } = json
        if (cardsResponse.length !== cards.length) {
            console.log("#### json ", cardsResponse)
            serCards(cardsResponse)
        }
        if (loading) {
            setLoading(false)
        }
        if (cardsResponse.length < 5) {
            new Promise((res) => { setTimeout(() => { getCards() }, 1500) })
        }
    }



    useEffect(() => {
        getCards()
    }, [])

    console.log("cards", cards)
    return <div className="z-10 w-full max-w-5xl items-center justify-between font-mono text-sm lg:flex">
        {cards.map(card => <Card card={card} key={card} />)}
        {/* loading ? "loading...." : <button
            onClick={async () => {
                try {
                    await fetch(cards.length < 5 ? "/api/cards/stop" : "/api/cards/start")
                }
                catch (e) {
                    console.error(e)
                }
            }
            } >
            {cards.length < 5 ? "Stop" : "Start"}
        </button> */}
    </div>

}

export default Main
