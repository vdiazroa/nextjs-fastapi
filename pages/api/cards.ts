import type { NextApiRequest, NextApiResponse } from 'next'
import fs from 'node:fs';
import path from 'path';


type ResponseData = {
    cards: string[]
}

export default function handler(
    req: NextApiRequest,
    res: NextApiResponse<ResponseData>
) {
    try {
        const data = fs.readFileSync(path.join(__dirname, "../../../../rfid/cards.txt"), 'utf8');
        const cards = data.split('\n').map(c => c.trim())
        console.log(data);
        res.status(200).json({ cards })

    } catch (err) {
        console.error(err);
        res.status(400).json({ cards: [] })

    }
}