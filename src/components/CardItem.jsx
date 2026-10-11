export default function CardItem({ card, onDelete }) {
  const isVisa = card.type === 'Visa'
  return (
    <div className={`p-6 rounded-2xl text-white shadow-lg relative overflow-hidden ${isVisa ? 'bg-gradient-to-br from-blue-600 to-indigo-700' : 'bg-gradient-to-br from-gray-800 to-black'}`}>
      <div className="absolute top-0 right-0 w-32 h-32 bg-white/10 rounded-full -mr-10 -mt-10"></div>
      <p className="text-sm opacity-80 mb-8">{card.type}</p>
      <p className="text-xl font-mono tracking-widest mb-4">{card.masked}</p>
      <div className="flex justify-between items-end">
        <div>
          <p className="text-xs opacity-70">Card Holder</p>
          <p className="font-semibold">{card.holder}</p>
        </div>
        <div>
          <p className="text-xs opacity-70">Expiry</p>
          <p className="font-semibold">{card.expiry}</p>
        </div>
      </div>
      {onDelete && (
        <button onClick={() => onDelete(card.id)} className="absolute top-4 right-4 text-xs bg-white/20 hover:bg-white/30 px-3 py-1 rounded-full">Delete</button>
      )}
    </div>
  )
}
