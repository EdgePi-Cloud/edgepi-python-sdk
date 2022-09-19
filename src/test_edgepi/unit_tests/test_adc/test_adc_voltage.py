"""Unit tests for adc_voltage.py module"""


import pytest
from edgepi.adc.adc_voltage import crc_8_atm, CRCCheckError

# pylint: disable=too-many-lines

@pytest.mark.parametrize("value, frame_len, expected", [
    (0x1961e331, 4, 0x84),
    (0x195f417b, 4, 0x8a),
    (0x1965abe2, 4, 0xeb),
    (0x19610b8d, 4, 0x52),
    (0x1967e781, 4, 0xb4),
    (0x1966c7a1, 4, 0x91),
    (0x196a959a, 4, 0xec),
    (0x1965d820, 4, 0x36),
    (0x19610fe3, 4, 0x0b),
    (0x1967fcc9, 4, 0x8b),
    (0x1965d2cb, 4, 0x2b),
    (0x1964eac3, 4, 0x29),
    (0x19656d9e, 4, 0x0b),
    (0x1965abb4, 4, 0x4e),
    (0x1964536f, 4, 0x96),
    (0x1967b500, 4, 0x1c),
    (0x1967d692, 4, 0x21),
    (0x19680bbb, 4, 0xea),
    (0x19646582, 4, 0x9c),
    (0x1968341b, 4, 0xb9),
    (0x1966ca7a, 4, 0x77),
    (0x1968db0c, 4, 0x5c),
    (0x196a615a, 4, 0xe2),
    (0x1965e7b5, 4, 0xee),
    (0x19634fe3, 4, 0x86),
    (0x196c9246, 4, 0xe0),
    (0x19655ed1, 4, 0x27),
    (0x19689a0e, 4, 0x1c),
    (0x1967e2bd, 4, 0x41),
    (0x1965eee4, 4, 0xe3),
    (0x1967847b, 4, 0x96),
    (0x1967e6fa, 4, 0xc7),
    (0x19677dbf, 4, 0x6d),
    (0x196608b4, 4, 0xd4),
    (0x1969eb87, 4, 0x76),
    (0x19605ffe, 4, 0x3f),
    (0x1962cbaf, 4, 0xec),
    (0x1967db5d, 4, 0xab),
    (0x1961ed43, 4, 0x0b),
    (0x1967a200, 4, 0x20),
    (0x1969eda8, 4, 0xc5),
    (0x196a3e55, 4, 0x00),
    (0x196861e9, 4, 0x24),
    (0x1969e20a, 4, 0x61),
    (0x19679e02, 4, 0x2b),
    (0x196713cb, 4, 0x05),
    (0x1965afdf, 4, 0x0c),
    (0x19670c08, 4, 0xd6),
    (0x196273c0, 4, 0x01),
    (0x1969574b, 4, 0xaf),
    (0x1966bfae, 4, 0xb6),
    (0x19653927, 4, 0x75),
    (0x196534e5, 4, 0xdc),
    (0x19667f01, 4, 0x1f),
    (0x19684ac0, 4, 0xc2),
    (0x19680934, 4, 0x64),
    (0x19632f59, 4, 0x5c),
    (0x19664114, 4, 0x5b),
    (0x19673088, 4, 0x5a),
    (0x1965a196, 4, 0x22),
    (0x19691d0b, 4, 0xb1),
    (0x1964fed7, 4, 0x46),
    (0x196aa45f, 4, 0x55),
    (0x196066f2, 4, 0x5f),
    (0x19612a4c, 4, 0xa0),
    (0x1963a7df, 4, 0xd9),
    (0x1965ec7e, 4, 0x06),
    (0x19676bd1, 4, 0x49),
    (0x19646b4e, 4, 0x20),
    (0x1968cdc7, 4, 0x0a),
    (0x196a30cf, 4, 0x19),
    (0x196acc8f, 4, 0x36),
    (0x19684823, 4, 0x4f),
    (0x19664597, 4, 0x8f),
    (0x1967e428, 4, 0xdd),
    (0x1967c2c7, 4, 0x8e),
    (0x196c04ab, 4, 0xf2),
    (0x196932e0, 4, 0x43),
    (0x19675e21, 4, 0x2f),
    (0x1964daad, 4, 0xdd),
    (0x1967d1cb, 4, 0xc2),
    (0x1967dba2, 4, 0x58),
    (0x1968931f, 4, 0xd6),
    (0x19682f96, 4, 0xd3),
    (0x1962cfaf, 4, 0xb8),
    (0x1967a73f, 4, 0xdc),
    (0x1966cefd, 4, 0xbf),
    (0x1967fdff, 4, 0x1c),
    (0x1965820b, 4, 0x69),
    (0x19643f02, 4, 0x9b),
    (0x1966a9f0, 4, 0x02),
    (0x1965ce70, 4, 0xa8),
    (0x196455df, 4, 0xf1),
    (0x195e949d, 4, 0xa6),
    (0x196800e8, 4, 0xc3),
    (0x1963e7e1, 4, 0x38),
    (0x1963ac29, 4, 0x82),
    (0x1968ca92, 4, 0xcd),
    (0x1965ed68, 4, 0x71),
    (0x196b0ee3, 4, 0x99),
    (0x1969b7cf, 4, 0x79),
    (0x19695a67, 4, 0x82),
    (0x19678836, 4, 0x8e),
    (0x1968f574, 4, 0x4b),
    (0x196a9aaa, 4, 0xbf),
    (0x196602c0, 4, 0x1d),
    (0x1969c1a1, 4, 0xa8),
    (0x19673d99, 4, 0xc4),
    (0x19679229, 4, 0x06),
    (0x1965223c, 4, 0xf4),
    (0x1968ab0e, 4, 0xf0),
    (0x1963ea3a, 4, 0xde),
    (0x196959c1, 4, 0xc6),
    (0x1966a29c, 4, 0x96),
    (0x1969520c, 4, 0x3c),
    (0x19661afb, 4, 0x43),
    (0x1965769a, 4, 0xd7),
    (0x19674414, 4, 0x71),
    (0x196b634d, 4, 0xc6),
    (0x1962f841, 4, 0xae),
    (0x196b2972, 4, 0xa2),
    (0x1965093a, 4, 0xdf),
    (0x19665923, 4, 0x21),
    (0x19663006, 4, 0x92),
    (0x1967b31b, 4, 0x23),
    (0x1965cef6, 4, 0x33),
    (0x19666519, 4, 0x82),
    (0x19693d1c, 4, 0x7a),
    (0x1966c3fe, 4, 0x5f),
    (0x196904a8, 4, 0x3b),
    (0x196bdb85, 4, 0x57),
    (0x19686499, 4, 0x32),
    (0x19698759, 4, 0x6b),
    (0x1965b465, 4, 0xe3),
    (0x196805b4, 4, 0x11),
    (0x19622096, 4, 0x97),
    (0x196881d5, 4, 0xd3),
    (0x1967dfed, 4, 0xe6),
    (0x1967e3ca, 4, 0x16),
    (0x195f2294, 4, 0xc3),
    (0x196510b9, 4, 0xb5),
    (0x19645c2a, 4, 0x89),
    (0x19625a20, 4, 0xbc),
    (0x19687797, 4, 0x70),
    (0x1969ea59, 4, 0x77),
    (0x19657d20, 4, 0x6f),
    (0x19656d20, 4, 0x38),
    (0x1967c9b3, 4, 0x52),
    (0x196711ab, 4, 0x08),
    (0x1964312d, 4, 0x80),
    (0x1968062c, 4, 0xef),
    (0x196613e4, 4, 0xa3),
    (0x1967048d, 4, 0xec),
    (0x196749d9, 4, 0xf5),
    (0x196c5ac1, 4, 0x39),
    (0x19689533, 4, 0x6c),
    (0x196ac75b, 4, 0x83),
    (0x1964bdfb, 4, 0xe6),
    (0x19634263, 4, 0xe6),
    (0x1967608b, 4, 0x5f),
    (0x1967c93d, 4, 0xf1),
    (0x1964ecea, 4, 0x88),
    (0x196a3df2, 4, 0x43),
    (0x19630a18, 4, 0x73),
    (0x1966c1f9, 4, 0x60),
    (0x196792c1, 4, 0x90),
    (0x19698b62, 4, 0x36),
    (0x1964b3e0, 4, 0x71),
    (0x1967d245, 4, 0x5e),
    (0x196b02db, 4, 0xcd),
    (0x19645f9f, 4, 0xb4),
    (0x1967291e, 4, 0x5b),
    (0x19671b0b, 4, 0xe3),
    (0x19661aa1, 4, 0xc2),
    (0x19674214, 4, 0x0f),
    (0x19637a80, 4, 0x10),
    (0x196a11b4, 4, 0xc4),
    (0x19677b28, 4, 0xff),
    (0x19683679, 4, 0xba),
    (0x19669677, 4, 0xa4),
    (0x19643d7d, 4, 0xcb),
    (0x196b693c, 4, 0x14),
    (0x1967801b, 4, 0xe5),
    (0x19671950, 4, 0x4f),
    (0x196975ff, 4, 0x2e),
    (0x1969043e, 4, 0xd0),
    (0x196b9e9b, 4, 0x17),
    (0x1962347f, 4, 0x05),
    (0x1966f925, 4, 0x2b),
    (0x19644a92, 4, 0x81),
    (0x1967956b, 4, 0xa4),
    (0x1969360c, 4, 0x9d),
    (0x1967b701, 4, 0x31),
    (0x19671079, 4, 0x2d),
    (0x196885d1, 4, 0x9b),
    (0x19669913, 4, 0x5c),
    (0x1967922e, 4, 0x13),
    (0x1966381c, 4, 0x7c),
    (0x196380ce, 4, 0x6b),
    (0x19671a3a, 4, 0x61),
    (0x1969b9cc, 4, 0xa6),
    (0x196772d3, 4, 0xad),
    (0x19693406, 4, 0x81),
    (0x1965f37b, 4, 0x89),
    (0x196b3525, 4, 0xab),
    (0x196923eb, 4, 0x30),
    (0x1969b4a0, 4, 0x4c),
    (0x1968979d, 4, 0x05),
    (0x1967b3ed, 4, 0xef),
    (0x196641cc, 4, 0x5d),
    (0x1969a5bc, 4, 0x5a),
    (0x19674c05, 4, 0xae),
    (0x196bbd59, 4, 0xc6),
    (0x196c6517, 4, 0x2f),
    (0x1968ce6f, 4, 0x64),
    (0x1965768a, 4, 0xa7),
    (0x196c7180, 4, 0xc0),
    (0x196cadeb, 4, 0x90),
    (0x196668ba, 4, 0x0b),
    (0x1968ad51, 4, 0x14),
    (0x196a83ee, 4, 0x8e),
    (0x196a424f, 4, 0x18),
    (0x1967ad4f, 4, 0x09),
    (0x19652c06, 4, 0x84),
    (0x1965e4c5, 4, 0x86),
    (0x1963f60b, 4, 0xe2),
    (0x196acb84, 4, 0x6c),
    (0x19673c04, 4, 0x0b),
    (0x1968e674, 4, 0x23),
    (0x1964c67d, 4, 0x48),
    (0x196720d9, 4, 0xbd),
    (0x19665c69, 4, 0x91),
    (0x196ad8b3, 4, 0x81),
    (0x196910d6, 4, 0x45),
    (0x196958b8, 4, 0xbb),
    (0x19665a45, 4, 0x2b),
    (0x196956fa, 4, 0xa4),
    (0x196914db, 4, 0x32),
    (0x196ac075, 4, 0x22),
    (0x196b4b0b, 4, 0x15),
    (0x196c4065, 4, 0x99),
    (0x196834cc, 4, 0x92),
    (0x1966501b, 4, 0x34),
    (0x196816bd, 4, 0x46),
    (0x19672159, 4, 0x21),
    (0x19656b41, 4, 0x66),
    (0x1964ba64, 4, 0x59),
    (0x19696d90, 4, 0xdb),
    (0x196809a8, 4, 0xb9),
    (0x196a23e9, 4, 0x83),
    (0x19674fa0, 4, 0xe3),
    (0x1968944b, 4, 0x16),
    (0x19665af5, 4, 0x32),
    (0x19680e96, 4, 0x68),
    (0x196c225e, 4, 0xe7),
    (0x1964edbb, 4, 0x2d),
    (0x196964e7, 4, 0x24),
    (0x196a0f5c, 4, 0xd3),
    (0x19682683, 4, 0x05),
    (0x196c8f3c, 4, 0x3f),
    (0x19631f70, 4, 0x7a),
    (0x1969962a, 4, 0x77),
    (0x19675e2c, 4, 0x0c),
    (0x1967460f, 4, 0x1a),
    (0x196a731c, 4, 0x4a),
    (0x19639920, 4, 0x05),
    (0x196a76ec, 4, 0xd5),
    (0x1965c60c, 4, 0x73),
    (0x1964f768, 4, 0xcf),
    (0x19656e42, 4, 0x2e),
    (0x19681c4c, 4, 0x1d),
    (0x19685f7a, 4, 0xfb),
    (0x19636cfc, 4, 0x4a),
    (0x196c2117, 4, 0x20),
    (0x19671cd2, 4, 0x89),
    (0x19675d8b, 4, 0x4f),
    (0x1968b651, 4, 0xd4),
    (0x196b4542, 4, 0x3b),
    (0x1969d47a, 4, 0xb1),
    (0x19681370, 4, 0x6a),
    (0x19690365, 4, 0x3d),
    (0x1969b1e9, 4, 0xf5),
    (0x19675f34, 4, 0x51),
    (0x1964d1e7, 4, 0xbb),
    (0x19699fe4, 4, 0xae),
    (0x196852fb, 4, 0x9c),
    (0x19691fe8, 4, 0x3c),
    (0x196acf39, 4, 0x02),
    (0x1968823b, 4, 0x68),
    (0x1968ea6c, 4, 0x97),
    (0x1967916f, 4, 0xec),
    (0x196dbb12, 4, 0x33),
    (0x1964cfc1, 4, 0xc8),
    (0x1966d9e4, 4, 0xcc),
    (0x1965ab0f, 4, 0x66),
    (0x19695e92, 4, 0x13),
    (0x19654f73, 4, 0x02),
    (0x196973cf, 4, 0xc0),
    (0x1969462c, 4, 0xdf),
    (0x1965a3be, 4, 0xd0),
    (0x196b8e15, 4, 0xe3),
    (0x19696c09, 4, 0x08),
    (0x196a57a4, 4, 0x91),
    (0x19644d3a, 4, 0xbb),
    (0x196a87c8, 4, 0x28),
    (0x19695774, 4, 0x12),
    (0x196c1750, 4, 0x75),
    (0x1967f186, 4, 0x88),
    (0x196793de, 4, 0xd8),
    (0x19680bc2, 4, 0x82),
    (0x196b3afe, 4, 0x67),
    (0x1962a826, 4, 0x90),
    (0x196a1310, 4, 0x9b),
    (0x196a3bc2, 4, 0xad),
    (0x196bf0d3, 4, 0xcb),
    (0x196bff33, 4, 0xa6),
    (0x19684015, 4, 0x65),
    (0x196cb879, 4, 0x71),
    (0x1965d6b8, 4, 0x21),
    (0x196affb4, 4, 0x51),
    (0x1961fa77, 4, 0xbb),
    (0x1967bb2c, 4, 0x0e),
    (0x19666caa, 4, 0x2f),
    (0x1969530c, 4, 0x29),
    (0x196ac711, 4, 0x72),
    (0x1968a958, 4, 0x7f),
    (0x19684b12, 4, 0xe7),
    (0x196487c4, 4, 0x20),
    (0x1968a935, 4, 0x7b),
    (0x196618ae, 4, 0xc5),
    (0x1965942b, 4, 0xa0),
    (0x19628b9f, 4, 0x27),
    (0x1967009b, 4, 0xda),
    (0x19682aa6, 4, 0x02),
    (0x19655dad, 4, 0x6b),
    (0x196393d7, 4, 0x4c),
    (0x19657e68, 4, 0xaf),
    (0x1968572f, 4, 0xff),
    (0x1968ca2b, 4, 0xeb),
    (0x196a6ac7, 4, 0xaf),
    (0x196bd4bc, 4, 0x3b),
    (0x1965c84e, 4, 0x6c),
    (0x196620e3, 4, 0x70),
    (0x1968941e, 4, 0xba),
    (0x1966a8c0, 4, 0x87),
    (0x19672dd6, 4, 0x79),
    (0x1966ce4e, 4, 0xaf),
    (0x196904e0, 4, 0xc4),
    (0x1964ac20, 4, 0xab),
    (0x1964a7f0, 4, 0x02),
    (0x19659797, 4, 0xa2),
    (0x1963ec7e, 4, 0x7b),
    (0x1967f8cb, 4, 0xd1),
    (0x196a1cc1, 4, 0x61),
    (0x196b0a9f, 4, 0xbe),
    (0x1968b385, 4, 0xb7),
    (0x1964f2e7, 4, 0x2a),
    (0x1959f1ec, 4, 0x54),
    (0x1964cdbf, 4, 0x9f),
    (0x19678381, 4, 0x15),
    (0x19632c61, 4, 0xcb),
    (0x19620bd5, 4, 0x60),
    (0x1968e1c4, 4, 0x51),
    (0x19661535, 4, 0xe4),
    (0x196ee5db, 4, 0x25),
    (0x1966a515, 4, 0x4b),
    (0x19682ab4, 4, 0x7c),
    (0x19645c95, 4, 0xbd),
    (0x196c8d77, 4, 0xe3),
    (0x1967536e, 4, 0x2c),
    (0x196824c8, 4, 0xd9),
    (0x196c7957, 4, 0x43),
    (0x196599d5, 4, 0xbd),
    (0x19679a5f, 4, 0xeb),
    (0x19686edd, 4, 0x6b),
    (0x19686d56, 4, 0xec),
    (0x196af7dc, 4, 0xe6),
    (0x196ba4a9, 4, 0xf2),
    (0x1969b181, 4, 0xea),
    (0x196af168, 4, 0x9d),
    (0x1964c9d3, 4, 0xc8),
    (0x19675294, 4, 0xd1),
    (0x19668bfa, 4, 0xb0),
    (0x196344bd, 4, 0x8c),
    (0x1966dc05, 4, 0x24),
    (0x1966577c, 4, 0x6d),
    (0x19642a88, 4, 0x32),
    (0x19670c71, 4, 0xbe),
    (0x19692051, 4, 0x20),
    (0x196fcd12, 4, 0x39),
    (0x1967fc7d, 4, 0x8e),
    (0x19698a12, 4, 0x74),
    (0x1962cb67, 4, 0x9a),
    (0x19681bdc, 4, 0x8f),
    (0x196694f2, 4, 0x1c),
    (0x19627ce4, 4, 0x3e),
    (0x19683527, 4, 0x18),
    (0x195fed77, 4, 0x4a),
    (0x196ad668, 4, 0x58),
    (0x1968f04c, 4, 0xa2),
    (0x19696797, 4, 0x4c),
    (0x196bd2c1, 4, 0x31),
    (0x196c28df, 4, 0xeb),
    (0x1967ee2c, 4, 0x43),
    (0x196b287d, 4, 0x9a),
    (0x196b6f3d, 4, 0x6d),
    (0x196a01bb, 4, 0xbe),
    (0x19642bcf, 4, 0xf5),
    (0x19698928, 4, 0xed),
    (0x1966e4e7, 4, 0xd5),
    (0x1969af31, 4, 0x72),
    (0x196a3833, 4, 0x4b),
    (0x196a1861, 4, 0x5c),
    (0x196a594d, 4, 0xd6),
    (0x1968cbf6, 4, 0xe3),
    (0x1966fdcb, 4, 0xfb),
    (0x1967cd74, 4, 0x5d),
    (0x196a682d, 4, 0x1d),
    (0x1965dfe0, 4, 0x13),
    (0x1964ddc8, 4, 0x8a),
    (0x196b3bb3, 4, 0x96),
    (0x19693668, 4, 0xa6),
    (0x19670f02, 4, 0xdf),
    (0x1965aad6, 4, 0x72),
    (0x1967f6f6, 4, 0xb4),
    (0x1966671c, 4, 0xb3),
    (0x19642741, 4, 0xaa),
    (0x19669fac, 4, 0x16),
    (0x1961758f, 4, 0x28),
    (0x19661184, 4, 0xae),
    (0x1968b81f, 4, 0xef),
    (0x196be24d, 4, 0x65),
    (0x1967cbe6, 4, 0xd4),
    (0x1966b643, 4, 0x86),
    (0x1969f962, 4, 0xbe),
    (0x196720fc, 4, 0x46),
    (0x196ce14c, 4, 0x4b),
    (0x19685b3f, 4, 0x73),
    (0x19682d0f, 4, 0x3f),
    (0x1968d548, 4, 0x51),
    (0x196929f8, 4, 0xcb),
    (0x1964458b, 4, 0x0d),
    (0x19684599, 4, 0x89),
    (0x1969998f, 4, 0xc6),
    (0x19688d75, 4, 0x46),
    (0x1968a2f6, 4, 0xab),
    (0x196bf933, 4, 0xd8),
    (0x196c0728, 4, 0x4d),
    (0x196830ee, 4, 0x28),
    (0x196beb87, 4, 0xa0),
    (0x19691836, 4, 0x43),
    (0x1967efd5, 4, 0xb7),
    (0x19691b0a, 4, 0xc8),
    (0x196a5263, 4, 0x8b),
    (0x1969928b, 4, 0x4d),
    (0x19615668, 4, 0x02),
    (0x1967698f, 4, 0xfe),
    (0x196be806, 4, 0x11),
    (0x196c3ba7, 4, 0xec),
    (0x196967e1, 4, 0x09),
    (0x196522f0, 4, 0x9e),
    (0x196a176d, 4, 0xbb),
    (0x196da56e, 4, 0xc1),
    (0x1967928a, 4, 0x66),
    (0x1966fcf3, 4, 0x46),
    (0x196640cb, 4, 0x5d),
    (0x1967de15, 4, 0x15),
    (0x19653a7a, 4, 0xde),
    (0x1966d293, 4, 0x19),
    (0x1964b604, 4, 0x82),
    (0x196af3f0, 4, 0x76),
    (0x19644f54, 4, 0x9c),
    (0x1968c6bd, 4, 0xfc),
    (0x19667d73, 4, 0x6c),
    (0x19697507, 4, 0xc8),
    (0x1969edb6, 4, 0x9f),
    (0x1965db90, 4, 0x10),
    (0x1969ee2f, 4, 0x66),
    (0x1967eefa, 4, 0x6f),
    (0x196b0264, 4, 0xf9),
    (0x19682eb9, 4, 0x0b),
    (0x1967f698, 4, 0xb9),
    (0x1963b76b, 4, 0x8b),
    (0x196bdcf6, 4, 0x62),
    (0x196b9329, 4, 0xe9),
    (0x196894c9, 4, 0x91),
    (0x19701374, 4, 0x85),
    (0x196859c1, 4, 0xad),
    (0x196968f5, 4, 0xa6),
    (0x1967db2d, 4, 0xfc),
    (0x1969fdae, 4, 0x80),
    (0x19669ba3, 4, 0x6f),
    (0x196a5778, 4, 0x8b),
    (0x196befc0, 4, 0x26),
    (0x19698b53, 4, 0xa1),
    (0x19682216, 4, 0xb3),
    (0x1967cfa4, 4, 0x49),
    (0x1965ed85, 4, 0xfc),
    (0x196b4a6a, 4, 0x20),
    (0x196a2994, 4, 0x75),
    (0x1965f962, 4, 0x44),
    (0x196597af, 4, 0x0a),
    (0x196e3894, 4, 0x9c),
    (0x19673e03, 4, 0x34),
    (0x196a8101, 4, 0x27),
    (0x19664e71, 4, 0xa4),
    (0x1965bd55, 4, 0xce),
    (0x196c970c, 4, 0x50),
    (0x196b716a, 4, 0x4e),
    (0x1969e54a, 4, 0xcd),
    (0x19667b3c, 4, 0xf8),
    (0x196c1669, 4, 0xcf),
    (0x19692bf8, 4, 0xe1),
    (0x1966a2f8, 4, 0xad),
    (0x196a4145, 4, 0x11),
    (0x196621e4, 4, 0x70),
    (0x196d90aa, 4, 0x2b),
    (0x196736a9, 4, 0xc3),
    (0x1967fb0d, 4, 0xb2),
    (0x196821b5, 4, 0xec),
    (0x1967c644, 4, 0x5a),
    (0x19692548, 4, 0x2e),
    (0x19693428, 4, 0x4b),
    (0x19648a12, 4, 0xe5),
    (0x196bd441, 4, 0xc6),
    (0x1968e90b, 4, 0x9a),
    (0x1968b313, 4, 0x5c),
    (0x196d7d33, 4, 0x47),
    (0x196a79a8, 4, 0xcd),
    (0x19669fa2, 4, 0x3c),
    (0x19655233, 4, 0x7b),
    (0x196a2d4e, 4, 0x29),
    (0x196a0c85, 4, 0xed),
    (0x196af3e1, 4, 0x01),
    (0x196ba979, 4, 0x25),
    (0x196844d3, 4, 0x6d),
    (0x1964e83f, 4, 0xf9),
    (0x1969600f, 4, 0xe6),
    (0x196bc24d, 4, 0xcb),
    (0x1968f90a, 4, 0xca),
    (0x1968cbdb, 4, 0x20),
    (0x196800bc, 4, 0x68),
    (0x196853e6, 4, 0xda),
    (0x1967f380, 4, 0xb0),
    (0x19628a84, 4, 0x73),
    (0x19672d74, 4, 0x1e),
    (0x196aa0d5, 4, 0xbe),
    (0x196c310a, 4, 0x24),
    (0x196a5d3d, 4, 0xd5),
    (0x19686c6a, 4, 0x4d),
    (0x19697586, 4, 0x46),
    (0x196793a7, 4, 0xb0),
    (0x19697b77, 4, 0x49),
    (0x1963f802, 4, 0x0b),
    (0x1967fe0a, 4, 0xe6),
    (0x196a6fb9, 4, 0x93),
    (0x196c5bb1, 4, 0x7b),
    (0x196644b8, 4, 0x57),
    (0x196aa7f0, 4, 0x2e),
    (0x1966a21e, 4, 0x11),
    (0x196c002f, 4, 0x33),
    (0x1969a26d, 4, 0x08),
    (0x196b337c, 4, 0x5d),
    (0x19689bfd, 4, 0xde),
    (0x196ac1e8, 4, 0xed),
    (0x19688914, 4, 0x32),
    (0x19685394, 4, 0x83),
    (0x196d9140, 4, 0xa6),
    (0x1969979c, 4, 0x69),
    (0x19698a9b, 4, 0xc2),
    (0x196b6345, 4, 0xfe),
    (0x196954e2, 4, 0xc6),
    (0x196a6800, 4, 0xde),
    (0x19671d20, 4, 0x4c),
    (0x196b0504, 4, 0xb5),
    (0x196c85c0, 4, 0x47),
    (0x196901f3, 4, 0xfc),
    (0x1964610c, 4, 0x6b),
    (0x196b41f0, 4, 0x78),
    (0x196a509f, 4, 0x5b),
    (0x19622cca, 4, 0xf8),
    (0x196a50c4, 4, 0xdd),
    (0x19685002, 4, 0x57),
    (0x1968628f, 4, 0x2e),
    (0x19687703, 4, 0x95),
    (0x1966fd9f, 4, 0x50),
    (0x196574c3, 4, 0x75),
    (0x196d8423, 4, 0x9e),
    (0x196a0c9a, 4, 0xb0),
    (0x196d4371, 4, 0xa1),
    (0x19691d35, 4, 0x0b),
    (0x196431d3, 4, 0x74),
    (0x196ab67f, 4, 0xc8),
    (0x196798cd, 4, 0x36),
    (0x19699247, 4, 0x27),
    (0x196b7ee3, 4, 0x3b),
    (0x196ee5cc, 4, 0x40),
    (0x1969b0ab, 4, 0x29),
    (0x1965d4a9, 4, 0x7c),
    (0x196851f4, 4, 0x8e),
    (0x1965ec7c, 4, 0x08),
    (0x196b719f, 4, 0x8b),
    (0x196b2c74, 4, 0xf1),
    (0x196bcd76, 4, 0xa9),
    (0x196c319f, 4, 0xc6),
    (0x1969ce10, 4, 0x75),
    (0x196ce2fe, 4, 0x63),
    (0x196ba2e1, 4, 0x73),
    (0x1970768f, 4, 0xde),
    (0x1967e58c, 4, 0xbd),
    (0x196a8984, 4, 0x1d),
    (0x196a651a, 4, 0x71),
    (0x1967fd84, 4, 0x7a),
    (0x1967f79d, 4, 0xb7),
    (0x19699698, 4, 0x60),
    (0x196b7741, 4, 0xe1),
    (0x196efd36, 4, 0x57),
    (0x19667e99, 4, 0xcb),
    (0x19667386, 4, 0x7f),
    (0x196a875d, 4, 0xca),
    (0x196c4311, 4, 0xed),
    (0x1967b14e, 4, 0xa5),
    (0x1969ef08, 4, 0x86),
    (0x196c1613, 4, 0xae),
    (0x1969d7ae, 4, 0xac),
    (0x196db2d1, 4, 0xc9),
    (0x19649652, 4, 0x89),
    (0x196635d6, 4, 0xed),
    (0x196d1036, 4, 0x40),
    (0x196ac038, 4, 0xc6),
    (0x196c38a6, 4, 0xd4),
    (0x19670293, 4, 0xc8),
    (0x1969c02d, 4, 0x10),
    (0x19682b57, 4, 0xce),
    (0x196c214d, 4, 0xa1),
    (0x1967d60c, 4, 0xf2),
    (0x196bbc76, 4, 0x1e),
    (0x196b0b3f, 4, 0xc2),
    (0x196b7d21, 4, 0x44),
    (0x19690e13, 4, 0x91),
    (0x196cdb2a, 4, 0x05),
    (0x19682e9d, 4, 0xf7),
    (0x196c65c0, 4, 0x04),
    (0x1969200e, 4, 0xba),
    (0x19691f5c, 4, 0x39),
    (0x1967f91c, 4, 0xef),
    (0x19669158, 4, 0x02),
    (0x196a2eda, 4, 0xf3),
    (0x196b4123, 4, 0x4f),
    (0x196749da, 4, 0xfc),
    (0x19681e6d, 4, 0xd0),
    (0x196a8b52, 4, 0x1b),
    (0x1963fd2d, 4, 0x87),
    (0x1963dfa9, 4, 0x96),
    (0x19694c26, 4, 0x6b),
    (0x196beb1d, 4, 0x6f),
    (0x19678c63, 4, 0x76),
    (0x196c3d5b, 4, 0x68),
    (0x196bb9fd, 4, 0xe7),
    (0x196b64b4, 4, 0x4c),
    (0x196c8c1d, 4, 0xe7),
    (0x1966fe2d, 4, 0x78),
    (0x19692e5f, 4, 0xdc),
    (0x196cad36, 4, 0x8d),
    (0x196a59ba, 4, 0x1d),
    (0x196a8338, 4, 0xa2),
    (0x1967b2d2, 4, 0x47),
    (0x1962d9d4, 4, 0xf7),
    (0x196a0d2b, 4, 0xbb),
    (0x1969df49, 4, 0xbf),
    (0x196bad73, 4, 0x47),
    (0x196bad41, 4, 0xd9),
    (0x19687924, 4, 0xb6),
    (0x1968cea4, 4, 0x1b),
    (0x1968f6f8, 4, 0xd9),
    (0x1968a826, 4, 0x17),
    (0x196a4a35, 4, 0xd1),
    (0x1967e167, 4, 0x76),
    (0x196935e0, 4, 0x28),
    (0x1965505b, 4, 0x4e),
    (0x19681bbf, 4, 0xa1),
    (0x196b30e6, 4, 0xad),
    (0x196562f3, 4, 0xcc),
    (0x196bcc1c, 4, 0xad),
    (0x196cb688, 4, 0x7e),
    (0x196a8784, 4, 0xcb),
    (0x196a637b, 4, 0x2f),
    (0x1965616c, 4, 0x27),
    (0x196463e0, 4, 0xcb),
    (0x1966e346, 4, 0xd0),
    (0x196b3194, 4, 0xe1),
    (0x196a5924, 4, 0xce),
    (0x19689439, 4, 0x4f),
    (0x1969bb74, 4, 0xad),
    (0x1968f83e, 4, 0x53),
    (0x196c98b6, 4, 0xbc),
    (0x196aee85, 4, 0x84),
    (0x196496f2, 4, 0xe0),
    (0x196a9684, 4, 0x89),
    (0x196b5e77, 4, 0x70),
    (0x196552e6, 4, 0x5e),
    (0x1968aa64, 4, 0xf4),
    (0x196896fd, 4, 0x37),
    (0x196c3aaa, 4, 0xda),
    (0x196d5ab8, 4, 0x3a),
    (0x196b0f0d, 4, 0x08),
    (0x196acd80, 4, 0x0e),
    (0x1968f728, 4, 0xf2),
    (0x196be8fa, 4, 0xeb),
    (0x196b2275, 4, 0x20),
    (0x196867fe, 4, 0x3f),
    (0x19676aeb, 4, 0xfa),
    (0x1968cedd, 4, 0x73),
    (0x19693062, 4, 0xee),
    (0x196c5c97, 4, 0xe2),
    (0x1969966c, 4, 0xa2),
    (0x196ef20a, 4, 0x20),
    (0x196b48d6, 4, 0x37),
    (0x196727fa, 4, 0x3f),
    (0x19661714, 4, 0x29),
    (0x196a9da2, 4, 0xec),
    (0x1968a7ff, 4, 0xd5),
    (0x19696107, 4, 0xcb),
    (0x19690add, 4, 0xa1),
    (0x1968927f, 4, 0xe4),
    (0x196bc59f, 4, 0x90),
    (0x196dd35f, 4, 0x8a),
    (0x1967c486, 4, 0x30),
    (0x1969dde3, 4, 0xca),
    (0x196a1b1f, 4, 0x1e),
    (0x1968243f, 4, 0x12),
    (0x196bdd5e, 4, 0x26),
    (0x196bc77d, 4, 0x1a),
    (0x196ad0d9, 4, 0x38),
    (0x196b2f8b, 4, 0x3d),
    (0x196a0f7c, 4, 0x33),
    (0x19697a36, 4, 0x9c),
    (0x196c73d1, 4, 0x5a),
    (0x1967fcce, 4, 0x9e),
    (0x19672a6b, 4, 0x28),
    (0x196641c0, 4, 0x79),
    (0x196892bc, 4, 0xa3),
    (0x196b84cf, 4, 0x69),
    (0x1966024c, 4, 0xb0),
    (0x1965773b, 4, 0xac),
    (0x1969be9e, 4, 0x74),
    (0x19689c02, 4, 0x46),
    (0x1965b151, 4, 0x2e),
    (0x196a4ad5, 4, 0x7f),
    (0x196b1f5e, 4, 0xe1),
    (0x1967af28, 4, 0x11),
    (0x196901ea, 4, 0xb3),
    (0x19624af2, 4, 0xdb),
    (0x19679c3a, 4, 0xa9),
    (0x196795c7, 4, 0xe9),
    (0x196911cd, 4, 0x11),
    (0x195cad20, 4, 0x0e),
    (0x195a6c0e, 4, 0x41),
    (0x196e76f3, 4, 0x23),
    (0x196ad684, 4, 0xd2),
    (0x196c1c9a, 4, 0x9a),
    (0x196b5b47, 4, 0xa1),
    (0x196b5670, 4, 0xcd),
    (0x196b42c4, 4, 0xcb),
    (0x19610135, 4, 0xf1),
    (0x19651a4b, 4, 0xe7),
    (0x196881d4, 4, 0xd4),
    (0x19694da4, 4, 0xf9),
    (0x1966cd1d, 4, 0x2e),
    (0x196b68c3, 4, 0xf2),
    (0x196933fc, 4, 0x02),
    (0x1966bfed, 4, 0x78),
    (0x1969abf2, 4, 0x61),
    (0x1968beaf, 4, 0x88),
    (0x19690d29, 4, 0x08),
    (0x196a5c45, 4, 0xaf),
    (0x19648b7a, 4, 0xef),
    (0x19686a60, 4, 0x05),
    (0x1966dd15, 4, 0x41),
    (0x196ceb3f, 4, 0x97),
    (0x19694985, 4, 0x4a),
    (0x19686acf, 4, 0x41),
    (0x1968b901, 4, 0xa0),
    (0x19690ba2, 4, 0xce),
    (0x196ab463, 4, 0xb6),
    (0x196af685, 4, 0x7b),
    (0x196af96e, 4, 0x27),
    (0x196e4bf1, 4, 0x3d),
    (0x196a1f89, 4, 0xa1),
    (0x1966cd50, 4, 0xca),
    (0x196c8469, 4, 0x04),
    (0x196807bf, 4, 0x0a),
    (0x196a289d, 4, 0x5f),
    (0x19634361, 4, 0xfd),
    (0x1968155c, 4, 0xd0),
    (0x196af75a, 4, 0x7d),
    (0x196bbe54, 4, 0xda),
    (0x196730b6, 4, 0xe0),
    (0x196d08c9, 4, 0x4c),
    (0x196aa824, 4, 0xcf),
    (0x196d8cf7, 4, 0x14),
    (0x1967d5f4, 4, 0x2b),
    (0x196deb63, 4, 0x6f),
    (0x19688893, 4, 0xbb),
    (0x196a85f5, 4, 0xb1),
    (0x196a5953, 4, 0x8c),
    (0x196eab57, 4, 0x05),
    (0x1967131c, 4, 0x2e),
    (0x196779d8, 4, 0x0b),
    (0x196b661f, 4, 0x3e),
    (0x196d2eb6, 4, 0xe6),
    (0x19678cfe, 4, 0xac),
    (0x19681a62, 4, 0xa9),
    (0x1968e3c0, 4, 0x67),
    (0x196922b6, 4, 0xb1),
    (0x196d983c, 4, 0x68),
    (0x196ad090, 4, 0xc0),
    (0x19676b25, 4, 0x8b),
    (0x19651003, 4, 0x9a),
    (0x1967308a, 4, 0x54),
    (0x196a0514, 4, 0xae),
    (0x1968f09f, 4, 0x95),
    (0x196bb008, 4, 0x9f),
    (0x19675b1b, 4, 0xc8),
    (0x196b783f, 4, 0x5f),
    (0x1967a9c9, 4, 0xc6),
    (0x1960f149, 4, 0xfd),
    (0x1962a606, 4, 0xa6),
    (0x196596dd, 4, 0x46),
    (0x19647f99, 4, 0x08),
    (0x1967ccc4, 4, 0x51),
    (0x1965f432, 4, 0x1a),
    (0x196a69d0, 4, 0xf5),
    (0x1966c1cb, 4, 0xfe),
    (0x196380ba, 4, 0x20),
    (0x196d7330, 4, 0x98),
    (0x196bd42d, 4, 0xc5),
    (0x196c40ea, 4, 0x3d),
    (0x1965cccb, 4, 0xaa),
    (0x196a91cf, 4, 0x14),
    (0x19660e62, 4, 0x86),
    (0x19699777, 4, 0xf6),
    (0x196770a1, 4, 0xde),
    (0x1965e179, 4, 0xfa),
    (0x19675444, 4, 0x91),
    (0x1964e50c, 4, 0x89),
    (0x196c8b9b, 4, 0x17),
    (0x196985d4, 4, 0xeb),
    (0x19655eea, 4, 0x86),
    (0x1961164b, 4, 0xb0),
    (0x196335c9, 4, 0x70),
    (0x196e57b1, 4, 0x51),
    (0x196dc7c1, 4, 0x5a),
    (0x196900a2, 4, 0x59),
    (0x1964905f, 4, 0xd4),
    (0x19687ab5, 4, 0x77),
    (0x19667fb5, 4, 0x1a),
    (0x19691eb3, 4, 0xaf),
    (0x1966dc02, 4, 0x31),
    (0x1964c074, 4, 0x09),
    (0x1969a085, 4, 0xb4),
    (0x19617a10, 4, 0x3f),
    (0x196a68bc, 4, 0xe3),
    (0x196bbd27, 4, 0xbb),
    (0x1965d788, 4, 0xa4),
    (0x19679d44, 4, 0xc1),
    (0x19683643, 4, 0x1c),
    (0x196bb0ec, 4, 0x2d),
    (0x196991d9, 4, 0xcb),
    (0x19655525, 4, 0x72),
    (0x196a0136, 4, 0x14),
    (0x19671ffc, 4, 0x7c),
    (0x19627725, 4, 0xe0),
    (0x19685d2f, 4, 0x7d),
    (0x196b54ff, 4, 0x43),
    (0x19659f17, 4, 0x83),
    (0x195fb39a, 4, 0x1d),
    (0x196561b9, 4, 0x02),
    (0x1969ef40, 4, 0x79),
    (0x1966ba14, 4, 0xd8),
    (0x1968ebc3, 4, 0xc6),
    (0x196977e7, 4, 0x4c),
    (0x196a0039, 4, 0x2c),
    (0x19682865, 4, 0x6f),
    (0x19694225, 4, 0xb4),
    (0x196bb9b9, 4, 0x3c),
    (0x1969a0f0, 4, 0xf8),
    (0x19676671, 4, 0xc9),
    (0x196ad62d, 4, 0x84),
    (0x196848dd, 4, 0xbb),
    (0x19699a9d, 4, 0x87),
    (0x1967d25b, 4, 0x04),
    (0x196916dd, 4, 0x0a),
    (0x196d0af0, 4, 0xc9),
    (0x196a9ac4, 4, 0xb2),
    (0x19673b5d, 4, 0xe8),
    (0x196d8bda, 4, 0xbc),
    (0x19690f0f, 4, 0xd0),
    (0x19693298, 4, 0x2c),
    (0x1969420a, 4, 0x79),
    (0x19674e0b, 4, 0xae),
    (0x19662a39, 4, 0xfa),
    (0x1966b7a0, 4, 0x34),
    (0x19697c16, 4, 0x02),
    (0x196991fa, 4, 0x22),
    (0x196822c9, 4, 0xa0),
    (0x19668ae9, 4, 0xdc),
    (0x19685259, 4, 0xfb),
    (0x1969613e, 4, 0x64),
    (0x19660a29, 4, 0x24),
    (0x196a6a2b, 4, 0x25),
    (0x19692360, 4, 0x88),
    (0x1968ce31, 4, 0xf9),
    (0x1966d9a6, 4, 0x05),
    (0x196b1c32, 4, 0xdd),
    (0x196b0ef6, 4, 0xf2),
    (0x1969fb28, 4, 0x65),
    (0x19663220, 4, 0x4a),
    (0x196bdcfe, 4, 0x5a),
    (0x19699a90, 4, 0xa4),
    (0x1967b485, 4, 0x9b),
    (0x196be9f6, 4, 0xda),
    (0x19639e09, 4, 0xb1),
    (0x196a943b, 4, 0x97),
    (0x1967c371, 4, 0x90),
    (0x19684580, 4, 0xc6),
    (0x1964e0a5, 4, 0x9e),
    (0x196b3cd6, 4, 0xc1),
    (0x1968f98a, 4, 0x43),
    (0x19650ae6, 4, 0xfa),
    (0x19695eae, 4, 0xa7),
    (0x196d4ab2, 4, 0x5b),
    (0x196863b0, 4, 0x86),
    (0x196d522d, 4, 0x70),
    (0x1969761a, 4, 0xa4),
    (0x1968b597, 4, 0xb7),
    (0x196af32f, 4, 0x65),
    (0x1963c18c, 4, 0xec),
    (0x196a81f3, 4, 0xf7),
    (0x196ac422, 4, 0xd4),
    (0x196abc7d, 4, 0x44),
    (0x19684b15, 4, 0xf2),
    (0x196512ef, 4, 0x3a),
    (0x19685e04, 4, 0x93),
    (0x196960ec, 4, 0x41),
    (0x19692db5, 4, 0x7b),
    (0x196bb2f0, 4, 0x53),
    (0x196d88bd, 4, 0xb1),
    (0x19697624, 4, 0x1e),
    (0x19679e1f, 4, 0x78),
    (0x196a4df9, 4, 0xd0),
    (0x196a41e3, 4, 0x6a),
    (0x1967f492, 4, 0xa5),
    (0x196594a9, 4, 0x27),
    (0x19680ba8, 4, 0x93),
    (0x196b8926, 4, 0x11),
    (0x1968686e, 4, 0x05),
    (0x19684d3c, 4, 0x53),
    (0x1969f5b2, 4, 0x7c),
    (0x1968224f, 4, 0x3b),
    (0x1967b316, 4, 0x00),
    (0x196b1ca4, 4, 0x36),
    (0x1969503d, 4, 0x81),
    (0x1967ebcc, 4, 0xac),
    (0x196810f1, 4, 0xdb),
    (0x19675450, 4, 0xfd),
    (0x19694e46, 4, 0x66),
    (0x1969a271, 4, 0x5c),
    (0x19680898, 4, 0x3c),
    (0x196a40ee, 4, 0x5c),
    (0x196952fd, 4, 0xe5),
    (0x1967956a, 4, 0xa3),
    (0x19694f45, 4, 0x7a),
    (0x196cbf42, 4, 0xbb),
    (0x19662bf7, 4, 0x8b),
    (0x196de87a, 4, 0x1f),
    (0x1967c495, 4, 0x49),
    (0x1961bd34, 4, 0x45),
    (0x1969a435, 4, 0xf9),
    (0x196dcc94, 4, 0x61),
    (0x196c4508, 4, 0xdc),
    (0x1966483d, 4, 0x39),
    (0x19663ace, 4, 0x66),
    (0x1966ef36, 4, 0x7b),
    (0x1966c586, 4, 0x4e),
    (0x196593e5, 4, 0xaf),
    (0x1966443a, 4, 0xd0),
    (0x1965e4eb, 4, 0x4c),
    (0x1968a7d5, 4, 0x03),
    (0x19677477, 4, 0xa6),
    (0x1967154d, 4, 0xe0),
    (0x196af0b9, 4, 0xb1),
    (0x19627629, 4, 0xd1),
    (0x195f339c, 4, 0xb9),
    (0x196221c6, 4, 0x35),
    (0x1965d8cb, 4, 0xa9),
    (0x19686b90, 4, 0xce),
    (0x196a0f09, 4, 0x7f),
    (0x19697525, 4, 0x26),
    (0x196a8bc1, 4, 0xeb),
])
def test_crc_8_atm_adc_1(value, frame_len, expected):
    assert crc_8_atm(value, frame_len*8, expected) == expected


@pytest.mark.parametrize("value, frame_len, expected", [
    (0x1961e332, 4, 0x84),
    (0x195f447b, 4, 0x8a),
    (0x1967abe2, 4, 0xeb),
    (0x19618b8d, 4, 0x52),
    (0x19675781, 4, 0xb4),
    (0x1933c7a1, 4, 0x91),
    (0x296a959a, 4, 0xec),
    (0x1865d820, 4, 0x36),
    (0x19610fe4, 4, 0x0b),
    (0x1967fbf9, 4, 0x8b),
    (0x1963d2cb, 4, 0x2b),
])
def test_crc_8_atm_adc_1_error(value, frame_len, expected):
    with pytest.raises(CRCCheckError):
        crc_8_atm(value, frame_len*8, expected)
