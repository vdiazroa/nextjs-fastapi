import { FC, useEffect, useState } from "react"

const Main: FC = () => {
    const [cards, serCards] = useState<string[]>([])


    const Card: FC<{ card: string }> = ({ card }) => {
        return <img
            src={`https://optcgplayer.com/images/EN/${card}.png`}
            alt={card}
            // className="dark:invert"
            width={"150PX"}
            height={"200px"}
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

            serCards(cardsResponse.map((card:string) => card.toUpperCase()))
        }
        if (cardsResponse.length < 5) {
            new Promise((res) => { setTimeout(() => {getCards()}, 3000) })
        }
    }



    useEffect(() => {
        getCards()
    },[])

    console.log("cards", cards)
    return <div className="z-10 w-full max-w-5xl items-center justify-between font-mono text-sm lg:flex">
        <div className="CACA">{cards.map(card => <Card card={card} key={card} />)}</div>
        <button onClick={async () => { fetch("/api/clear") }} >
            clear
        </button>
    </div>

}

export default Main