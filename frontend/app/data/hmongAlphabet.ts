export interface HmongLetterDetail {
  letter: string;
  lao: string;
  category: string;
  ipa?: string;
  soundLike: string;
  exampleHmong: string;
  exampleLao: string;
  exampleMeaning: string;
  description: string;
  image?: string;
}

export const hmongAlphabetData: Record<string, HmongLetterDetail> = {
  // 1-LETTER CONSONANTS
  c: {
    letter: 'c',
    lao: 'ຈ',
    category: '1-Letter Consonant (Txiv Ntawv)',
    ipa: '/c/',
    soundLike: 'ຄືຕົວ "ຈ" (Unaspirated palatal)',
    exampleHmong: 'Cuaj',
    exampleLao: 'ຈວາ (ເລກ 9)',
    exampleMeaning: 'Nine (9)',
    image: '/images/letters/c.jpg',
    description: 'ຕົວ "c" ໃນ RPA ກົງກັບຕົວ "ຈ" ໃນພາສາລາວ (ບໍ່ພົ່ນລົມ). ຕົວຢ່າງ: Cuaj = ເລກ 9 (Nine).'
  },
  d: {
    letter: 'd',
    lao: 'ດ',
    category: '1-Letter Consonant (Txiv Ntawv)',
    ipa: '/d/',
    soundLike: 'ຄືຕົວ "ດ" (Voiced dental stop)',
    exampleHmong: 'Dej',
    exampleLao: 'ດ໊ຽ (ນ້ຳ)',
    exampleMeaning: 'Water (ນ້ຳ)',
    image: '/images/letters/d.jpg',
    description: 'ຕົວ "d" ໃນ RPA ກົງກັບຕົວ "ດ" ໃນພາສາລາວ ແລະ ພາສາອັງກິດ. ຕົວຢ່າງ: Dej = ນ້ຳ (Water).'
  },
  f: {
    letter: 'f',
    lao: 'ຟ',
    category: '1-Letter Consonant (Txiv Ntawv)',
    ipa: '/f/',
    soundLike: 'ຄືຕົວ "ຟ" (Labiodental fricative)',
    exampleHmong: 'Foob',
    exampleLao: 'ຟົ່ງ (ໃສ່ຮ້າຍ)',
    exampleMeaning: 'To accuse / frame',
    description: 'ຕົວ "f" ໃນ RPA ກົງກັບຕົວ "ຟ" ໃນພາສາລາວ.'
  },
  h: {
    letter: 'h',
    lao: 'ຮ / ຫ',
    category: '1-Letter Consonant (Txiv Ntawv)',
    ipa: '/h/',
    soundLike: 'ຄືຕົວ "ຮ" ຫຼື "ຫ" (Glottal fricative)',
    exampleHmong: 'Haus',
    exampleLao: 'ເຮົາ (ດື່ມ)',
    exampleMeaning: 'To drink',
    description: 'ຕົວ "h" ໃນ RPA ກົງກັບຕົວ "ຮ" ຫຼື "ຫ" ໃນພາສາລາວ.'
  },
  k: {
    letter: 'k',
    lao: 'ກ',
    category: '1-Letter Consonant (Txiv Ntawv)',
    ipa: '/k/',
    soundLike: 'ຄືຕົວ "ກ" (Unaspirated velar stop)',
    exampleHmong: 'Koob',
    exampleLao: 'ກົ່ງ (ເຂັມ)',
    exampleMeaning: 'Needle / Medal',
    description: 'ຕົວ "k" ໃນ RPA ກົງກັບຕົວ "ກ" ໃນພາສາລາວ (ສຽງ ກ ບໍ່ພົ່ນລົມ).'
  },
  l: {
    letter: 'l',
    lao: 'ລ',
    category: '1-Letter Consonant (Txiv Ntawv)',
    ipa: '/l/',
    soundLike: 'ຄືຕົວ "ລ" (Alveolar lateral)',
    exampleHmong: 'Lub',
    exampleLao: 'ລົ່ງ (ໜ່ວຍ)',
    exampleMeaning: 'Classifier (round object / item)',
    description: 'ຕົວ "l" ໃນ RPA ກົງກັບຕົວ "ລ" ໃນພາສາລາວ.'
  },
  m: {
    letter: 'm',
    lao: 'ມ',
    category: '1-Letter Consonant (Txiv Ntawv)',
    ipa: '/m/',
    soundLike: 'ຄືຕົວ "ມ" (Bilabial nasal)',
    exampleHmong: 'Me',
    exampleLao: 'ເມ (ນ້ອຍ)',
    exampleMeaning: 'Small / Little',
    description: 'ຕົວ "m" ໃນ RPA ກົງກັບຕົວ "ມ" ໃນພາສາລາວ.'
  },
  n: {
    letter: 'n',
    lao: 'ນ',
    category: '1-Letter Consonant (Txiv Ntawv)',
    ipa: '/n/',
    soundLike: 'ຄືຕົວ "ນ" (Alveolar nasal)',
    exampleHmong: 'Neeg',
    exampleLao: 'ເນ່ງ (ຄົນ)',
    exampleMeaning: 'Person / Human',
    description: 'ຕົວ "n" ໃນ RPA ກົງກັບຕົວ "ນ" ໃນພາສາລາວ.'
  },
  p: {
    letter: 'p',
    lao: 'ປ',
    category: '1-Letter Consonant (Txiv Ntawv)',
    ipa: '/p/',
    soundLike: 'ຄືຕົວ "ປ" (Unaspirated bilabial stop)',
    exampleHmong: 'Paj',
    exampleLao: 'ປ່າ (ດອກໄມ້)',
    exampleMeaning: 'Flower (ດອກໄມ້)',
    image: '/images/letters/p.jpg',
    description: 'ຕົວ "p" ໃນ RPA ກົງກັບຕົວ "ປ" ໃນພາສາລາວ (ສຽງ ປ ບໍ່ພົ່ນລົມ). ຕົວຢ່າງ: Paj = ດອກໄມ້ (Flower).'
  },
  q: {
    letter: 'q',
    lao: 'ກ (ເລິກ)',
    category: '1-Letter Consonant (Txiv Ntawv)',
    ipa: '/q/',
    soundLike: 'ສຽງ "ກ" ອອກຈາກໂຄນລີ້ນເລິກ (Uvular stop)',
    exampleHmong: 'Qab',
    exampleLao: 'ກັ່ງ (ຫວານ / ໄກ່)',
    exampleMeaning: 'Sweet / Chicken / Bottom',
    description: 'ຕົວ "q" ເປັນສຽງ ກ ທີ່ອອກຈາກໂຄນລີ້ນເລິກໃນລຳຄໍ (ລິ້ນໄກ່).'
  },
  r: {
    letter: 'r',
    lao: 'ດຣ / ຈ (ງໍ້ລີ້ນ)',
    category: '1-Letter Consonant (Txiv Ntawv)',
    ipa: '/ʈ/',
    soundLike: 'ງໍ້ປາຍລີ້ນແຕະເພດານປາກ (Retroflex stop)',
    exampleHmong: 'Rooj',
    exampleLao: 'ຣົ່ງ (ໂຕະ)',
    exampleMeaning: 'Table',
    description: 'ຕົວ "r" ໃນ RPA ອອກສຽງໂດຍການງໍ້ປາຍລີ້ນຂຶ້ນແຕະເພດານປາກ.'
  },
  s: {
    letter: 's',
    lao: 'ຊ (ງໍ້ລີ້ນ)',
    category: '1-Letter Consonant (Txiv Ntawv)',
    ipa: '/ʂ/',
    soundLike: 'ສຽງ "ຊ" ງໍ້ປາຍລີ້ນ (Retroflex fricative)',
    exampleHmong: 'Su',
    exampleLao: 'ຊູ (ອາຫານທ່ຽງ)',
    exampleMeaning: 'Lunch',
    description: 'ຕົວ "s" ໃນ RPA ອອກສຽງ ຊ ແບບງໍ້ປາຍລີ້ນຂຶ້ນ.'
  },
  t: {
    letter: 't',
    lao: 'ຕ',
    category: '1-Letter Consonant (Txiv Ntawv)',
    ipa: '/t/',
    soundLike: 'ຄືຕົວ "ຕ" (Unaspirated dental stop)',
    exampleHmong: 'Tes',
    exampleLao: 'ເຕ (ມື)',
    exampleMeaning: 'Hand / Arm',
    description: 'ຕົວ "t" ໃນ RPA ກົງກັບຕົວ "ຕ" ໃນພາສາລາວ (ສຽງ ຕ ບໍ່ພົ່ນລົມ).'
  },
  v: {
    letter: 'v',
    lao: 'ວ',
    category: '1-Letter Consonant (Txiv Ntawv)',
    ipa: '/v/',
    soundLike: 'ຄືຕົວ "ວ" (Voiced labiodental)',
    exampleHmong: 'Vaj',
    exampleLao: 'ວ່່າ (ສວນ)',
    exampleMeaning: 'Garden / Yard',
    description: 'ຕົວ "v" ໃນ RPA ກົງກັບຕົວ "ວ" ໃນພາສາລາວ.'
  },
  x: {
    letter: 'x',
    lao: 'ສ / ຊ',
    category: '1-Letter Consonant (Txiv Ntawv)',
    ipa: '/s/',
    soundLike: 'ຄືຕົວ "ສ" ຫຼື "ຊ" ປົກກະຕິ (Alveolar fricative)',
    exampleHmong: 'Xov',
    exampleLao: 'ສໍ (ຂ່າວ)',
    exampleMeaning: 'News / Message',
    description: 'ຕົວ "x" ໃນ RPA ກົງກັບຕົວ "ສ" ຫຼື "ຊ" ແບບລີ້ນຮາບພຽງ.'
  },
  y: {
    letter: 'y',
    lao: 'ຢ',
    category: '1-Letter Consonant (Txiv Ntawv)',
    ipa: '/j/',
    soundLike: 'ຄືຕົວ "ຢ" (Palatal approximant)',
    exampleHmong: 'Yeej',
    exampleLao: 'ຢຽງ (ຊະນະ)',
    exampleMeaning: 'To win / Definitely',
    description: 'ຕົວ "y" ໃນ RPA ກົງກັບຕົວ "ຢ" ໃນພາສາລາວ.'
  },
  z: {
    letter: 'z',
    lao: 'ຊ (ສຽງກ້ອງ)',
    category: '1-Letter Consonant (Txiv Ntawv)',
    ipa: '/ʐ/',
    soundLike: 'ສຽງ "ຊ" ກ້ອງໃນລຳຄໍງໍ້ລີ້ນ (Voiced retroflex)',
    exampleHmong: 'Zoo',
    exampleLao: 'ຊົ່ງ (ດີ)',
    exampleMeaning: 'Good / Beautiful',
    description: 'ຕົວ "z" ແມ່ນສຽງຄູ່ກ້ອງ (voiced) ຂອງຕົວ s ແບບງໍ້ປາຍລີ້ນ.'
  },

  // 2-LETTER CONSONANTS
  ch: {
    letter: 'ch',
    lao: 'ຊ / ຈ (ພົ່ນລົມ)',
    category: '2-Letter Consonant (Txiv Ntawv)',
    ipa: '/cʰ/',
    soundLike: 'ສຽງ "ຈ" ພົ່ນລົມ (Aspirated palatal)',
    exampleHmong: 'Chaw',
    exampleLao: 'ຊໍ (ບ່ອນ)',
    exampleMeaning: 'Place / Spot',
    description: 'ຕົວ "ch" ອອກສຽງຄື ຈ ພ້ອມພົ່ນລົມອອກມາ.'
  },
  dh: {
    letter: 'dh',
    lao: 'ດ (ພົ່ນລົມ)',
    category: '2-Letter Consonant (Txiv Ntawv)',
    ipa: '/dʱ/',
    soundLike: 'ສຽງ "ດ" ມີລົມກ້ອງ (Breathy dental)',
    exampleHmong: 'Dhas',
    exampleLao: 'ດ່າ (ຖູ)',
    exampleMeaning: 'To scrape / brush',
    description: 'ຕົວ "dh" ແມ່ນສຽງ ດ ທີ່ມີລົມກ້ອງຕາມມາ.'
  },
  hl: {
    letter: 'hl',
    lao: 'ຫຼ',
    category: '2-Letter Consonant (Txiv Ntawv)',
    ipa: '/ɬ/',
    soundLike: 'ຄືຕົວ "ຫຼ" (Voiceless lateral)',
    exampleHmong: 'Hli',
    exampleLao: 'ຫຼີ (ເດືອນ)',
    exampleMeaning: 'Moon / Month',
    description: 'ຕົວ "hl" ກົງກັບຕົວ "ຫຼ" ໃນພາສາລາວ ພົ່ນລົມອອກສອງຂ້າງລີ້ນ.'
  },
  hm: {
    letter: 'hm',
    lao: 'ໝ',
    category: '2-Letter Consonant (Txiv Ntawv)',
    ipa: '/m̥/',
    soundLike: 'ຄືຕົວ "ໝ" (Voiceless nasal)',
    exampleHmong: 'Hmoov',
    exampleLao: 'ໝົ່ງ (ໂຊກ)',
    exampleMeaning: 'Luck / Fortune',
    description: 'ຕົວ "hm" ກົງກັບຕົວ "ໝ" ໃນພາສາລາວ ອອກສຽງ ມ ພົ່ນລົມ.'
  },
  hn: {
    letter: 'hn',
    lao: 'ໜ',
    category: '2-Letter Consonant (Txiv Ntawv)',
    ipa: '/n̥/',
    soundLike: 'ຄືຕົວ "ໜ" (Voiceless nasal)',
    exampleHmong: 'Hnub',
    exampleLao: 'ໜົ່ງ (ມື້/ຕາເວັນ)',
    exampleMeaning: 'Sun / Day',
    description: 'ຕົວ "hn" ກົງກັບຕົວ "ໜ" ໃນພາສາລາວ ອອກສຽງ ນ ພົ່ນລົມ.'
  },
  kh: {
    letter: 'kh',
    lao: 'ຄ / ຂ',
    category: '2-Letter Consonant (Txiv Ntawv)',
    ipa: '/kʰ/',
    soundLike: 'ຄືຕົວ "ຄ" ຫຼື "ຂ" (Aspirated velar)',
    exampleHmong: 'Khab',
    exampleLao: 'ຂັ່ງ (ຕ້ອນຮັບ)',
    exampleMeaning: 'Guest / Welcome',
    description: 'ຕົວ "kh" ກົງກັບຕົວ "ຄ" ຫຼື "ຂ" ພົ່ນລົມ.'
  },
  ml: {
    letter: 'ml',
    lao: 'ມລ',
    category: '2-Letter Consonant (Txiv Ntawv)',
    ipa: '/ml/',
    soundLike: 'ສຽງຄວບ "ມ" ແລະ "ລ"',
    exampleHmong: 'Mlob',
    exampleLao: 'ມລົ່ງ (ຫ່ຽວ)',
    exampleMeaning: 'Wilted / Drooping',
    description: 'ຕົວ "ml" ອອກສຽງ ມ ຄວບ ລ.'
  },
  nc: {
    letter: 'nc',
    lao: 'ນຈ',
    category: '2-Letter Consonant (Txiv Ntawv)',
    ipa: '/ɲc/',
    soundLike: 'ສຽງ "ນ" ນຳໜ້າ "ຈ"',
    exampleHmong: 'Ncas',
    exampleLao: 'ນຈ່າ',
    exampleMeaning: 'Jaw harp',
    description: 'ຕົວ "nc" ເປັນສຽງ prenasalized ຂອງ ຈ.'
  },
  nk: {
    letter: 'nk',
    lao: 'ນກ',
    category: '2-Letter Consonant (Txiv Ntawv)',
    ipa: '/ŋk/',
    soundLike: 'ສຽງ "ງ/ນ" ນຳໜ້າ "ກ"',
    exampleHmong: 'Nkauj',
    exampleLao: 'ນເກົ່າ (ສາວ/ເພງ)',
    exampleMeaning: 'Girl / Song',
    description: 'ຕົວ "nk" ອອກສຽງ ນ/ງ ຕິດໜ້າ ກ.'
  },
  np: {
    letter: 'np',
    lao: 'ມປ / ບ',
    category: '2-Letter Consonant (Txiv Ntawv)',
    ipa: '/mp/',
    soundLike: 'ສຽງ "ມ" ນຳໜ້າ "ປ"',
    exampleHmong: 'Npua',
    exampleLao: 'ມປົວ (ໝູ)',
    exampleMeaning: 'Pig (ໝູ)',
    image: '/images/letters/np.jpg',
    description: 'ຕົວ "np" ອອກສຽງ ມ ນຳໜ້າ ປ (ຄ້າຍ ບ ແໜ້ນ). ຕົວຢ່າງ: Npua = ໝູ (Pig).'
  },
  nq: {
    letter: 'nq',
    lao: 'ນກ (ເລິກ)',
    category: '2-Letter Consonant (Txiv Ntawv)',
    ipa: '/ɴq/',
    soundLike: 'ສຽງ "ນ" ນຳໜ້າ "q" ໂຄນລີ້ນ',
    exampleHmong: 'Nqaij',
    exampleLao: 'ນໄກ່ (ຊີ້ນ)',
    exampleMeaning: 'Meat / Flesh',
    description: 'ຕົວ "nq" ເປັນສຽງ prenasalized ຂອງ q ໂຄນລີ້ນ.'
  },
  nr: {
    letter: 'nr',
    lao: 'ນດຣ',
    category: '2-Letter Consonant (Txiv Ntawv)',
    ipa: '/ɳʈ/',
    soundLike: 'ສຽງ "ນ" ນຳໜ້າ retroflex r',
    exampleHmong: 'Nruab',
    exampleLao: 'ນດຣົ່ງ (ລະຫວ່າງ)',
    exampleMeaning: 'Middle / Between',
    description: 'ຕົວ "nr" ອອກສຽງ ນ ນຳໜ້າ r ງໍ້ລີ້ນ.'
  },
  nt: {
    letter: 'nt',
    lao: 'ນຕ',
    category: '2-Letter Consonant (Txiv Ntawv)',
    ipa: '/nt/',
    soundLike: 'ສຽງ "ນ" ນຳໜ້າ "ຕ"',
    exampleHmong: 'Ntawv',
    exampleLao: 'ນເຕົາ (ປຶ້ມ)',
    exampleMeaning: 'Book / Paper',
    description: 'ຕົວ "nt" ອອກສຽງ ນ ນຳໜ້າ ຕ.'
  },
  ny: {
    letter: 'ny',
    lao: 'ຍ',
    category: '2-Letter Consonant (Txiv Ntawv)',
    ipa: '/ɲ/',
    soundLike: 'ຄືຕົວ "ຍ" (Palatal nasal)',
    exampleHmong: 'Nyooj',
    exampleLao: 'ຍົ່ງ (ຮ້ອງຄາງ)',
    exampleMeaning: 'To roar / groan',
    description: 'ຕົວ "ny" ກົງກັບຕົວ "ຍ" ໃນພາສາລາວ.'
  },
  ph: {
    letter: 'ph',
    lao: 'ຜ / ພ',
    category: '2-Letter Consonant (Txiv Ntawv)',
    ipa: '/pʰ/',
    soundLike: 'ຄືຕົວ "ຜ" ຫຼື "ພ" (Aspirated bilabial)',
    exampleHmong: 'Phau',
    exampleLao: 'ເຜົາ (ຫົວ/ເຫຼັ້ມ)',
    exampleMeaning: 'Classifier for books',
    description: 'ຕົວ "ph" ກົງກັບຕົວ "ຜ" ຫຼື "ພ" ໃນພາສາລາວ.'
  },
  pl: {
    letter: 'pl',
    lao: 'ປລ',
    category: '2-Letter Consonant (Txiv Ntawv)',
    ipa: '/pl/',
    soundLike: 'ສຽງຄວບ "ປ" ແລະ "ລ"',
    exampleHmong: 'Plau',
    exampleLao: 'ເປົາ (ແລ່ນໜີ)',
    exampleMeaning: 'To run away / husk',
    description: 'ຕົວ "pl" ອອກສຽງ ປ ຄວບ ລ.'
  },
  qh: {
    letter: 'qh',
    lao: 'ຂ (ເລິກ)',
    category: '2-Letter Consonant (Txiv Ntawv)',
    ipa: '/qʰ/',
    soundLike: 'ສຽງ "q" ແບບພົ່ນລົມເລິກໃນຄໍ',
    exampleHmong: 'Qhov',
    exampleLao: 'ຂໍ (ຮູ/ບ່ອນ)',
    exampleMeaning: 'Hole / Place',
    description: 'ຕົວ "qh" ແມ່ນສຽງ q ທີ່ພົ່ນລົມອອກມາເລິກໃນຄໍ.'
  },
  rh: {
    letter: 'rh',
    lao: 'ທຣ (ງໍ້ລີ້ນ)',
    category: '2-Letter Consonant (Txiv Ntawv)',
    ipa: '/ʈʰ/',
    soundLike: 'ສຽງ "r" ງໍ້ລີ້ນແບບພົ່ນລົມ',
    exampleHmong: 'Rhaub',
    exampleLao: 'ທເຣົາ (ຕົ້ມ)',
    exampleMeaning: 'To boil',
    description: 'ຕົວ "rh" ອອກສຽງ r ງໍ້ລີ້ນ ພ້ອມພົ່ນລົມ.'
  },
  th: {
    letter: 'th',
    lao: 'ຖ / ທ',
    category: '2-Letter Consonant (Txiv Ntawv)',
    ipa: '/tʰ/',
    soundLike: 'ຄືຕົວ "ຖ" ຫຼື "ທ" (Aspirated dental)',
    exampleHmong: 'Thaum',
    exampleLao: 'ເຖົາ (ເວລາ)',
    exampleMeaning: 'When / Time',
    description: 'ຕົວ "th" ກົງກັບຕົວ "ຖ" ຫຼື "ທ" ໃນພາສາລາວ.'
  },
  ts: {
    letter: 'ts',
    lao: 'ຕສ',
    category: '2-Letter Consonant (Txiv Ntawv)',
    ipa: '/ts/',
    soundLike: 'ສຽງ affricate ຄວບ "ຕ" ແລະ "ສ"',
    exampleHmong: 'Tsev',
    exampleLao: 'ຕເຊັວ (ເຮືອນ)',
    exampleMeaning: 'House / Home',
    description: 'ຕົວ "ts" ອອກສຽງ ຕ ຄວບ ສ ພ້ອມກັນ.'
  },
  tx: {
    letter: 'tx',
    lao: 'ຕຊ',
    category: '2-Letter Consonant (Txiv Ntawv)',
    ipa: '/ts/',
    soundLike: 'ສຽງ affricate ຄວບ "ຕ" ແລະ "ຊ"',
    exampleHmong: 'Txiv',
    exampleLao: 'ຕຊີ່ (ພໍ່/ໝາກ)',
    exampleMeaning: 'Father / Fruit / Husband',
    description: 'ຕົວ "tx" ອອກສຽງ ຕ ຄວບ ຊ.'
  },
  xy: {
    letter: 'xy',
    lao: 'ຊຍ',
    category: '2-Letter Consonant (Txiv Ntawv)',
    ipa: '/ɕ/',
    soundLike: 'ສຽງ "ຊ" ປະສົມ "ຍ"',
    exampleHmong: 'Xyoo',
    exampleLao: 'ຊຢອງ (ປີ)',
    exampleMeaning: 'Year',
    description: 'ຕົວ "xy" ອອກສຽງ ຊ ຄວບ ຍ.'
  },

  // 3-LETTER CONSONANTS
  hml: {
    letter: 'hml',
    lao: 'ໝລ',
    category: '3-Letter Consonant (Txiv Ntawv)',
    ipa: '/m̥l/',
    soundLike: 'ສຽງ ໝ ຄວບ ລ',
    exampleHmong: 'Hmla',
    exampleLao: 'ໝລາ (ຕົກໃຈ)',
    exampleMeaning: 'Startled / Amazed',
    description: 'ສຽງ ໝ ຄວບ ລ ພົ່ນລົມ.'
  },
  hny: {
    letter: 'hny',
    lao: 'ໜຍ',
    category: '3-Letter Consonant (Txiv Ntawv)',
    ipa: '/ɲ̥/',
    soundLike: 'ສຽງ ໜ ຄວບ ຍ',
    exampleHmong: 'Hnyos',
    exampleLao: 'ໜຍໍ (ຍິ້ມ)',
    exampleMeaning: 'Smile',
    description: 'ສຽງ ຍ ພົ່ນລົມ.'
  },
  nch: {
    letter: 'nch',
    lao: 'ນຊ',
    category: '3-Letter Consonant (Txiv Ntawv)',
    ipa: '/ɲcʰ/',
    soundLike: 'ສຽງ ນ ນຳໜ້າ ch',
    exampleHmong: 'Ncho',
    exampleLao: 'ນຊໍ (ຄວັນ)',
    exampleMeaning: 'Smoke / Steam',
    description: 'ສຽງ prenasalized ຂອງ ch.'
  },
  nkh: {
    letter: 'nkh',
    lao: 'ນຄ',
    category: '3-Letter Consonant (Txiv Ntawv)',
    ipa: '/ŋkʰ/',
    soundLike: 'ສຽງ ນ ນຳໜ້າ kh',
    exampleHmong: 'Nkhaus',
    exampleLao: 'ນເຂົາ (ຄົດ)',
    exampleMeaning: 'Bent / Crooked',
    description: 'ສຽງ prenasalized ຂອງ kh.'
  },
  nph: {
    letter: 'nph',
    lao: 'ມພ',
    category: '3-Letter Consonant (Txiv Ntawv)',
    ipa: '/mpʰ/',
    soundLike: 'ສຽງ ມ ນຳໜ້າ ph',
    exampleHmong: 'Nphoo',
    exampleLao: 'ມພອງ (ຫວ່ານ)',
    exampleMeaning: 'To sprinkle / scatter',
    description: 'ສຽງ prenasalized ຂອງ ph.'
  },
  npl: {
    letter: 'npl',
    lao: 'ມປລ',
    category: '3-Letter Consonant (Txiv Ntawv)',
    ipa: '/mpl/',
    soundLike: 'ສຽງ ມ ນຳໜ້າ pl',
    exampleHmong: 'Nplooj',
    exampleLao: 'ມປລົ່ງ (ໃບໄມ້)',
    exampleMeaning: 'Leaf',
    description: 'ສຽງ prenasalized ຂອງ pl.'
  },
  nqh: {
    letter: 'nqh',
    lao: 'ນຂ (ເລິກ)',
    category: '3-Letter Consonant (Txiv Ntawv)',
    ipa: '/ɴqʰ/',
    soundLike: 'ສຽງ ນ ນຳໜ້າ qh',
    exampleHmong: 'Nqhes',
    exampleLao: 'ນເຂ (ຫິວນ້ຳ)',
    exampleMeaning: 'Thirsty',
    description: 'ສຽງ prenasalized ຂອງ qh.'
  },
  nrh: {
    letter: 'nrh',
    lao: 'ນທຣ',
    category: '3-Letter Consonant (Txiv Ntawv)',
    ipa: '/ɳʈʰ/',
    soundLike: 'ສຽງ ນ ນຳໜ້າ rh',
    exampleHmong: 'Nrho',
    exampleLao: 'ນທຣໍ (ຢຸດ)',
    exampleMeaning: 'To stop completely',
    description: 'ສຽງ prenasalized ຂອງ rh.'
  },
  nth: {
    letter: 'nth',
    lao: 'ນທ',
    category: '3-Letter Consonant (Txiv Ntawv)',
    ipa: '/ntʰ/',
    soundLike: 'ສຽງ ນ ນຳໜ້າ th',
    exampleHmong: 'Ntho',
    exampleLao: 'ນທໍ (ຈັບ/ຄວ້າ)',
    exampleMeaning: 'To snatch / seize',
    description: 'ສຽງ prenasalized ຂອງ th.'
  },
  nts: {
    letter: 'nts',
    lao: 'ນຕສ',
    category: '3-Letter Consonant (Txiv Ntawv)',
    ipa: '/nts/',
    soundLike: 'ສຽງ ນ ນຳໜ້າ ts',
    exampleHmong: 'Ntse',
    exampleLao: 'ນຕເຊ (ສະຫຼາດ)',
    exampleMeaning: 'Smart / Sharp',
    description: 'ສຽງ prenasalized ຂອງ ts.'
  },
  ntx: {
    letter: 'ntx',
    lao: 'ນຕຊ',
    category: '3-Letter Consonant (Txiv Ntawv)',
    ipa: '/nts/',
    soundLike: 'ສຽງ ນ ນຳໜ້າ tx',
    exampleHmong: 'Ntxhais',
    exampleLao: 'ນຕຊາຍ (ລູກສາວ)',
    exampleMeaning: 'Daughter / Girl',
    description: 'ສຽງ prenasalized ຂອງ tx.'
  },
  plh: {
    letter: 'plh',
    lao: 'ພລ',
    category: '3-Letter Consonant (Txiv Ntawv)',
    ipa: '/pʰl/',
    soundLike: 'ສຽງ ພ ຄວບ ລ',
    exampleHmong: 'Plhos',
    exampleLao: 'ພລໍ (ຫຼຸດ)',
    exampleMeaning: 'To slip off',
    description: 'ສຽງ pl ແບບພົ່ນລົມ.'
  },
  tsh: {
    letter: 'tsh',
    lao: 'ທສ',
    category: '3-Letter Consonant (Txiv Ntawv)',
    ipa: '/tsʰ/',
    soundLike: 'ສຽງ ທ ຄວບ ສ',
    exampleHmong: 'Tshav',
    exampleLao: 'ທສັວ (ແດດ)',
    exampleMeaning: 'Sunshine',
    description: 'ສຽງ ts ແບບພົ່ນລົມ.'
  },
  txh: {
    letter: 'txh',
    lao: 'ທຊ',
    category: '3-Letter Consonant (Txiv Ntawv)',
    ipa: '/tsʰ/',
    soundLike: 'ສຽງ ທ ຄວບ ຊ',
    exampleHmong: 'Txheeb',
    exampleLao: 'ທເຊັງ (ຍາດພີ່ນ້ອງ)',
    exampleMeaning: 'Relatives / Kin',
    description: 'ສຽງ tx ແບບພົ່ນລົມ.'
  },

  // 4-LETTER CONSONANTS
  nplh: {
    letter: 'nplh',
    lao: 'ມພລ',
    category: '4-Letter Consonant (Txiv Ntawv)',
    ipa: '/mpʰl/',
    soundLike: 'ສຽງ ມ ນຳໜ້າ plh',
    exampleHmong: 'Nplhaib',
    exampleLao: 'ມພລາຍ (ແຫວນ)',
    exampleMeaning: 'Ring (jewelry)',
    description: 'ສຽງ prenasalized ຂອງ plh.'
  },
  ntsh: {
    letter: 'ntsh',
    lao: 'ນທສ',
    category: '4-Letter Consonant (Txiv Ntawv)',
    ipa: '/ntsʰ/',
    soundLike: 'ສຽງ ນ ນຳໜ້າ tsh',
    exampleHmong: 'Ntshai',
    exampleLao: 'ນທສາຍ (ຢ້ານ)',
    exampleMeaning: 'Afraid / Fear',
    description: 'ສຽງ prenasalized ຂອງ tsh.'
  },
  ntxh: {
    letter: 'ntxh',
    lao: 'ນທຊ',
    category: '4-Letter Consonant (Txiv Ntawv)',
    ipa: '/ntsʰ/',
    soundLike: 'ສຽງ ນ ນຳໜ້າ txh',
    exampleHmong: 'Ntxhoo',
    exampleLao: 'ນທຊອງ (ຮົ່ມເຢັນ)',
    exampleMeaning: 'Shady / Cool shade',
    description: 'ສຽງ prenasalized ຂອງ txh.'
  },

  // 1-LETTER VOWELS
  a: {
    letter: 'a',
    lao: 'ອາ',
    category: '1-Letter Vowel (Niam Suab)',
    ipa: '/a/',
    soundLike: 'ສະຫຼະ ອາ',
    exampleHmong: 'Av',
    exampleLao: 'ອັວ (ດິນ)',
    exampleMeaning: 'Soil / Earth',
    description: 'ສະຫຼະ ອາ ສຽງກາງຮາບພຽງ.'
  },
  e: {
    letter: 'e',
    lao: 'ເອ',
    category: '1-Letter Vowel (Niam Suab)',
    ipa: '/e/',
    soundLike: 'ສະຫຼະ ເອ',
    exampleHmong: 'Es',
    exampleLao: 'ເອ່ (ແລະ/ແລ້ວ)',
    exampleMeaning: 'And / So',
    description: 'ສະຫຼະ ເອ ສຽງກາງ.'
  },
  i: {
    letter: 'i',
    lao: 'ອີ',
    category: '1-Letter Vowel (Niam Suab)',
    ipa: '/i/',
    soundLike: 'ສະຫຼະ ອີ',
    exampleHmong: 'Ib',
    exampleLao: 'ອີ່ (ໜຶ່ງ/1)',
    exampleMeaning: 'One (1)',
    description: 'ສະຫຼະ ອີ ສຽງຍາວ.'
  },
  o: {
    letter: 'o',
    lao: 'ອໍ',
    category: '1-Letter Vowel (Niam Suab)',
    ipa: '/ɔ/',
    soundLike: 'ສະຫຼະ ອໍ',
    exampleHmong: 'Ob',
    exampleLao: 'ອໍ່ (ສອງ/2)',
    exampleMeaning: 'Two (2)',
    description: 'ສະຫຼະ ອໍ ສຽງກາງ.'
  },
  u: {
    letter: 'u',
    lao: 'ອູ',
    category: '1-Letter Vowel (Niam Suab)',
    ipa: '/u/',
    soundLike: 'ສະຫຼະ ອູ',
    exampleHmong: 'Ua',
    exampleLao: 'ອົວ (ເຮັດ)',
    exampleMeaning: 'To do / make',
    description: 'ສະຫຼະ ອູ ສຽງປາກມົນ.'
  },
  w: {
    letter: 'w',
    lao: 'ອື',
    category: '1-Letter Vowel (Niam Suab)',
    ipa: '/ɨ/',
    soundLike: 'ສະຫຼະ ອື',
    exampleHmong: 'Wb',
    exampleLao: 'ອື່ (ພວກເຮົາສອງ)',
    exampleMeaning: 'We two (dual)',
    description: 'ສະຫຼະ ອື (High central unrounded).'
  },

  // 2-LETTER VOWELS
  aa: {
    letter: 'aa',
    lao: 'ອັງ / າງ',
    category: '2-Letter Vowel (Niam Suab)',
    ipa: '/aŋ/',
    soundLike: 'ສະຫຼະ ອັງ / າງ',
    exampleHmong: 'Aas',
    exampleLao: 'ອ່າງ',
    exampleMeaning: 'Duck / Swallow',
    description: 'ສະຫຼະ ອາ ປະສົມຕົວສະກົດ ງ.'
  },
  ai: {
    letter: 'ai',
    lao: 'ໄອ',
    category: '2-Letter Vowel (Niam Suab)',
    ipa: '/ai/',
    soundLike: 'ສະຫຼະ ໄອ',
    exampleHmong: 'Ais',
    exampleLao: 'ໄອ່ (ນ້ຳກ້ອນ)',
    exampleMeaning: 'Ice',
    description: 'ສະຫຼະ ປະສົມ ອາ + ອີ.'
  },
  au: {
    letter: 'au',
    lao: 'ເອົາ',
    category: '2-Letter Vowel (Niam Suab)',
    ipa: '/au/',
    soundLike: 'ສະຫຼະ ເອົາ',
    exampleHmong: 'Aub',
    exampleLao: 'ເອົ່າ (ໝາ)',
    exampleMeaning: 'Dog',
    description: 'ສະຫຼະ ປະສົມ ອາ + ອູ.'
  },
  aw: {
    letter: 'aw',
    lao: 'ເອົາ (ສັ້ນ)',
    category: '2-Letter Vowel (Niam Suab)',
    ipa: '/aɨ/',
    soundLike: 'ສະຫຼະ ເອົາສັ້ນ',
    exampleHmong: 'Awg',
    exampleLao: 'ເອົາ (ໝູ່)',
    exampleMeaning: 'Friend / Buddy',
    description: 'ສະຫຼະ ປະສົມ ອາ + ອື.'
  },
  ee: {
    letter: 'ee',
    lao: 'ແອງ / ເອັງ',
    category: '2-Letter Vowel (Niam Suab)',
    ipa: '/eŋ/',
    soundLike: 'ສະຫຼະ ເອັງ / ແອງ',
    exampleHmong: 'Eeb',
    exampleLao: 'ເອັ່ງ (ອານມ້າ)',
    exampleMeaning: 'Saddle',
    description: 'ສະຫຼະ ເອ ປະສົມຕົວສະກົດ ງ.'
  },
  ia: {
    letter: 'ia',
    lao: 'ເອັຍ / ອຽ',
    category: '2-Letter Vowel (Niam Suab)',
    ipa: '/iə/',
    soundLike: 'ສະຫຼະ ອຽ',
    exampleHmong: 'Iab',
    exampleLao: 'ອ່ຽ (ຂົມ)',
    exampleMeaning: 'Bitter',
    description: 'ສະຫຼະ ປະສົມ ອີ + ອາ.'
  },
  oo: {
    letter: 'oo',
    lao: 'ອອງ',
    category: '2-Letter Vowel (Niam Suab)',
    ipa: '/ɔŋ/',
    soundLike: 'ສະຫຼະ ອອງ',
    exampleHmong: 'Oob',
    exampleLao: 'ອ່ອງ (ຟູ)',
    exampleMeaning: 'To float / swell',
    description: 'ສະຫຼະ ອໍ ປະສົມຕົວສະກົດ ງ.'
  },
  ua: {
    letter: 'ua',
    lao: 'ອົວ',
    category: '2-Letter Vowel (Niam Suab)',
    ipa: '/uə/',
    soundLike: 'ສະຫຼະ ອົວ',
    exampleHmong: 'Uas',
    exampleLao: 'ອົ່ວ (ທີ່/ເຊິ່ງ)',
    exampleMeaning: 'That / Which',
    description: 'ສະຫຼະ ປະສົມ ອູ + ອາ.'
  },

  // TONES (CIM SUAB) - Namespaced to avoid key collisions with consonants (d, m, s, v)
  tone_b: {
    letter: 'b',
    lao: 'ສຽງໂທ (High level)',
    category: 'Tone Marker (Cim Suab)',
    ipa: '˥ (55)',
    soundLike: 'ສຽງສູງສະເໝີ (ຄືສຽງ ໂທ)',
    exampleHmong: 'Pob',
    exampleLao: 'ປົ່ງ (ກ້ອນ)',
    exampleMeaning: 'Ball / Lump',
    description: 'ສຽງວັນນະຍຸດລະດັບສູງຮາບພຽງ ຄືສຽງວັນນະຍຸດ ໂທ ໃນພາສາລາວ.'
  },
  tone_m: {
    letter: 'm',
    lao: 'ສຽງເອກສັ້ນ (Low glottalized)',
    category: 'Tone Marker (Cim Suab)',
    ipa: '˨˩ˀ (21ˀ)',
    soundLike: 'ສຽງຕ່ຳສັ້ນຕັດທ້າຍ',
    exampleHmong: 'Pom',
    exampleLao: 'ປ້ອມ (ເຫັນ)',
    exampleMeaning: 'To see',
    description: 'ສຽງຕ່ຳສັ້ນ ຕັດທ້າຍດ້ວຍສຽງກັກໃນລຳຄໍ (Glottal stop).'
  },
  tone_d: {
    letter: 'd',
    lao: 'ສຽງຂຶ້ນຕ່ຳ (Low rising)',
    category: 'Tone Marker (Cim Suab)',
    ipa: '˨˦ (24)',
    soundLike: 'ສຽງເລີ່ມຕ່ຳແລ້ວຂຶ້ນເລັກນ້ອຍ',
    exampleHmong: 'Pod',
    exampleLao: 'ປອດ (ກ້ອນນັ້ນ)',
    exampleMeaning: 'That lump over there',
    description: 'ສຽງເລີ່ມຕົ້ນຕ່ຳ ແລ້ວໂຄ້ງສູງຂຶ້ນ (Low rising tone).'
  },
  tone_j: {
    letter: 'j',
    lao: 'ສຽງຕີ (High falling)',
    category: 'Tone Marker (Cim Suab)',
    ipa: '˥˨ (52)',
    soundLike: 'ສຽງສູງແລ້ວຕົກລົງໄວ (ຄືສຽງ ຕີ)',
    exampleHmong: 'Poj',
    exampleLao: 'ປ໊ຽ (ແມ່ເຖົ້າ)',
    exampleMeaning: 'Elder woman / Female',
    description: 'ສຽງເລີ່ມຕົ້ນສູງຫຼາຍ ແລ້ວຕົກລົງມາໄວ.'
  },
  tone_v: {
    letter: 'v',
    lao: 'ສຽງຈັດຕະວາ (Mid rising)',
    category: 'Tone Marker (Cim Suab)',
    ipa: '˧˦ (34)',
    soundLike: 'ສຽງເລີ່ມກາງແລ້ວຂຶ້ນສູງ (ຄືສຽງ ຈັດຕະວາ)',
    exampleHmong: 'Pov',
    exampleLao: 'ປົວ (ໂຍນ)',
    exampleMeaning: 'To throw / toss',
    description: 'ສຽງເລີ່ມຕົ້ນລະດັບກາງ ແລ້ວໂຄ້ງຂຶ້ນສູງ.'
  },
  tone_s: {
    letter: 's',
    lao: 'ສຽງເອກ (Low level)',
    category: 'Tone Marker (Cim Suab)',
    ipa: '˩ (11)',
    soundLike: 'ສຽງຕ່ຳຮາບພຽງ (ຄືສຽງ ເອກ)',
    exampleHmong: 'Pos',
    exampleLao: 'ປໍ່ (ໜາມ)',
    exampleMeaning: 'Thorn',
    description: 'ສຽງວັນນະຍຸດລະດັບຕ່ຳສະເໝີ ຄ້າຍສຽງ ເອກ ໃນພາສາລາວ.'
  },
  tone_g: {
    letter: 'g',
    lao: 'ສຽງຫາຍໃຈ (Breathy falling)',
    category: 'Tone Marker (Cim Suab)',
    ipa: '˧˩̤ (31̤)',
    soundLike: 'ສຽງຕົກລົງພ້ອມພົ່ນລົມຫາຍໃຈ',
    exampleHmong: 'Pog',
    exampleLao: 'ປໍ (ຍ່າ)',
    exampleMeaning: 'Paternal grandmother',
    description: 'ສຽງລະດັບກາງຕົກລົງມາ ພ້ອມສຽງພົ່ນລົມຫາຍໃຈ (Breathy tone).'
  },
  tone_blank: {
    letter: '∅',
    lao: 'ສຽງສາມັນ (Mid level)',
    category: 'Tone Marker (Cim Suab)',
    ipa: '˧ (33)',
    soundLike: 'ສຽງກາງຮາບພຽງ (ສຽງສາມັນ)',
    exampleHmong: 'Po',
    exampleLao: 'ປໍ (ມ້າມ)',
    exampleMeaning: 'Spleen',
    description: 'ສຽງລະດັບກາງຮາບພຽງ (ສຽງສາມັນ) ບໍ່ມີພະຍັນຊະນະທ້າຍກຳກັບສຽງ.'
  },
  'tone_∅': {
    letter: '∅',
    lao: 'ສຽງສາມັນ (Mid level)',
    category: 'Tone Marker (Cim Suab)',
    ipa: '˧ (33)',
    soundLike: 'ສຽງກາງຮາບພຽງ (ສຽງສາມັນ)',
    exampleHmong: 'Po',
    exampleLao: 'ປໍ (ມ້າມ)',
    exampleMeaning: 'Spleen',
    description: 'ສຽງລະດັບກາງຮາບພຽງ (ສຽງສາມັນ) ບໍ່ມີພະຍັນຊະນະທ້າຍກຳກັບສຽງ.'
  }
};

export function generateLetterSvg(item: HmongLetterDetail): string {
  const displayUpper = item.letter.toUpperCase();
  const displayLao = item.lao;
  const categoryShort = item.category.split('(')[0].trim();
  
  const svg = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 280" width="100%" height="100%">
    <defs>
      <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="#001833" />
        <stop offset="50%" stop-color="#002b5c" />
        <stop offset="100%" stop-color="#091a2e" />
      </linearGradient>
      <linearGradient id="accent" x1="0%" y1="0%" x2="100%" y2="0%">
        <stop offset="0%" stop-color="#df1a72" />
        <stop offset="100%" stop-color="#ffd9e1" />
      </linearGradient>
      <radialGradient id="glow1" cx="20%" cy="30%" r="60%">
        <stop offset="0%" stop-color="#df1a72" stop-opacity="0.35" />
        <stop offset="100%" stop-color="#df1a72" stop-opacity="0" />
      </radialGradient>
      <radialGradient id="glow2" cx="80%" cy="70%" r="60%">
        <stop offset="0%" stop-color="#3b82f6" stop-opacity="0.3" />
        <stop offset="100%" stop-color="#3b82f6" stop-opacity="0" />
      </radialGradient>
      <pattern id="pattern-grid" width="32" height="32" patternUnits="userSpaceOnUse">
        <path d="M 32 0 L 0 0 0 32" fill="none" stroke="rgba(255,255,255,0.04)" stroke-width="1"/>
      </pattern>
    </defs>

    <!-- Background Layers -->
    <rect width="640" height="280" rx="20" fill="url(#bg)" />
    <rect width="640" height="280" rx="20" fill="url(#pattern-grid)" />
    <circle cx="160" cy="90" r="140" fill="url(#glow1)" />
    <circle cx="500" cy="180" r="150" fill="url(#glow2)" />
    <rect x="1" y="1" width="638" height="278" rx="19" fill="none" stroke="rgba(255,255,255,0.12)" stroke-width="1.5" />

    <!-- Top Badge -->
    <g transform="translate(320, 36)">
      <rect x="-130" y="-14" width="260" height="28" rx="14" fill="rgba(255,255,255,0.1)" stroke="rgba(255,255,255,0.15)" stroke-width="1"/>
      <text x="0" y="5" fill="#d6e3ff" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" font-weight="700" text-anchor="middle" letter-spacing="2">${categoryShort.toUpperCase()}</text>
    </g>

    <!-- Main Comparison: C = ຈ -->
    <g transform="translate(320, 142)">
      <!-- RPA Letter -->
      <text x="-105" y="24" fill="#ffffff" font-family="'Outfit', -apple-system, sans-serif" font-size="78" font-weight="900" text-anchor="middle" filter="drop-shadow(0 4px 8px rgba(0,0,0,0.5))">${displayUpper}</text>
      
      <!-- Equal Sign -->
      <text x="0" y="20" fill="url(#accent)" font-family="'Outfit', -apple-system, sans-serif" font-size="52" font-weight="800" text-anchor="middle">=</text>
      
      <!-- Lao Script -->
      <text x="105" y="24" fill="#ffd9e1" font-family="'Noto Sans Lao', 'Saysettha OT', -apple-system, sans-serif" font-size="74" font-weight="900" text-anchor="middle" filter="drop-shadow(0 4px 8px rgba(0,0,0,0.5))">${displayLao}</text>
    </g>

    <!-- Bottom Example Pill -->
    <g transform="translate(320, 235)">
      <rect x="-190" y="-17" width="380" height="34" rx="17" fill="rgba(0,0,0,0.3)" stroke="rgba(255,255,255,0.08)" stroke-width="1"/>
      <text x="0" y="5" fill="#9cf2e8" font-family="-apple-system, BlinkMacSystemFont, 'Noto Sans Lao', sans-serif" font-size="15" font-weight="600" text-anchor="middle">
        ຕົວຢ່າງ: ${item.exampleHmong} ↔ ${item.exampleLao} (${item.exampleMeaning})
      </text>
    </g>
  </svg>`;

  return 'data:image/svg+xml;utf8,' + encodeURIComponent(svg);
}
