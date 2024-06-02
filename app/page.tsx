import { FC, useEffect, useState } from "react"
import Image from "next/image";
import Link from "next/link";

export default function Home(): JSX.Element {
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
    const { cards, reading } = (await res.json())
    serCards(cards)
    setLoading(false)
    setReading(reading)

    if (reading) {
      await new Promise((res) => { setTimeout(() => res(true), 500) })
      getCards()
    }
  }



  useEffect(() => {
    getCards()
  }, [])

  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      <div className="z-10 w-full max-w-5xl items-center justify-between font-mono text-sm lg:flex">
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
    </main>
  );
}
