function Logo() {
  return (
    <svg width="36" height="36" viewBox="0 0 36 36" fill="none" xmlns="http://www.w3.org/2000/svg">
      {/* Cercle jeton */}
      <circle cx="18" cy="18" r="17" stroke="url(#goldGradient)" strokeWidth="2"/>
      <circle cx="18" cy="18" r="13" stroke="url(#goldGradient)" strokeWidth="0.5" strokeDasharray="3 2"/>
      
      {/* Fond jeton */}
      <circle cx="18" cy="18" r="16" fill="url(#bgGradient)"/>
      
      {/* As de pique */}
      <text x="18" y="23" textAnchor="middle" fontSize="18" fill="url(#goldGradient)" fontWeight="700" fontFamily="serif">♠</text>

      <defs>
        <linearGradient id="goldGradient" x1="0" y1="0" x2="36" y2="36">
          <stop offset="0%" stopColor="#f0c060"/>
          <stop offset="50%" stopColor="#c9a84c"/>
          <stop offset="100%" stopColor="#f0c060"/>
        </linearGradient>
        <linearGradient id="bgGradient" x1="0" y1="0" x2="36" y2="36">
          <stop offset="0%" stopColor="#1a1a2e"/>
          <stop offset="100%" stopColor="#0d0d18"/>
        </linearGradient>
      </defs>
    </svg>
  )
}

export default Logo