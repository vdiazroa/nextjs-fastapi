import { FC, useEffect, useState } from "react"
import Image from "next/image";
import Link from "next/link";

const Main: FC = () => {
    const [loading, setLoading] = useState<boolean>(true)
    const [reading, setReading] = useState<boolean>(false)
    const [cards, serCards] = useState<string[]>([])


    const Card: FC<{ card: string }> = ({ card }) => {
        return <Image
            src={`https://optcgplayer.com/images/EN/${card}.png`}
            alt={card}
            // className="dark:invert"
            width={30}
        />
    }

    const getCards = async () => {
        console.log("#### fetching cards")
        const res = await fetch("/api/cards")
        console.log("#### res",res)
        const json = (await res.json())
        console.log("#### json ",json)
        setLoading(false)

        const { cards, reading } = json
        serCards(cards)
        setReading(reading)

        if (reading) {
            await new Promise((res) => { setTimeout(() => res(true), 500) })
            getCards()
        }
    }



    useEffect(() => {
        getCards()
    }, [])

    return <div className="z-10 w-full max-w-5xl items-center justify-between font-mono text-sm lg:flex">
        <Link href="/api/cards">
        click </Link>
        {cards.map(card => <Card card={card} />)}
        {!loading ? "loading...." : <button
            onClick={async () => {
                await fetch(reading ? "/api/cards/stop" : "/api/cards/start?cards=5")
                setReading(!reading)
                if (reading) { getCards() }
            }
            } >
            {reading ? "Stop" : "Start"}
        </button>}
    </div>

}

export default Main