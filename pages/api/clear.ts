import type { NextApiRequest, NextApiResponse } from 'next'
import  fs  from 'fs';
import path from 'path';
 
type ResponseData = {
  message: string
}
 
export default function handler(
  _req: NextApiRequest,
  res: NextApiResponse<ResponseData>
) {
  fs.unlinkSync(path.join(__dirname, "../../../../rfid/cards.txt"))
  fs.writeFileSync(path.join(__dirname, "../../../../rfid/cards.txt"),"")
  res.status(200).json({ message: 'Hello from Next.js!' })
}