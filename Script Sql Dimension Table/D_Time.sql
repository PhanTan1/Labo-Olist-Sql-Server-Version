USE Olist_DW
GO

CREATE TABLE [dbo].[DimTime](

[TimeKey] [int] NOT NULL,

[Hour24] [int] NULL,

[Hour24ShortString] [varchar](2) NULL,

[Hour24MinString] [varchar](5) NULL,

[Hour24FullString] [varchar](8) NULL,

[Hour12] [int] NULL,

[Hour12ShortString] [varchar](2) NULL,

[Hour12MinString] [varchar](5) NULL,

[Hour12FullString] [varchar](8) NULL,

[AmPmCode] [int] NULL,

[AmPmString] [varchar](2) NOT NULL,

[Minute] [int] NULL,

[MinuteCode] [int] NULL,

[MinuteShortString] [varchar](2) NULL,

[MinuteFullString24] [varchar](8) NULL,

[MinuteFullString12] [varchar](8) NULL,

[HalfHour] [int] NULL,

[HalfHourCode] [int] NULL,

[HalfHourShortString] [varchar](2) NULL,

[HalfHourFullString24] [varchar](8) NULL,

[HalfHourFullString12] [varchar](8) NULL,

[Second] [int] NULL,

[SecondShortString] [varchar](2) NULL,

[FullTimeString24] [varchar](8) NULL,

[FullTimeString12] [varchar](8) NULL,

[FullTime] [time](7) NULL,

CONSTRAINT [PK_DimTime] PRIMARY KEY CLUSTERED

(

[TimeKey] ASC

)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]

) ON [PRIMARY]

GO

declare @hour int

declare @minute int

declare @second int

set @hour=0

while @hour<24

begin

set @minute=0

while @minute<60

begin

set @second=0

while @second<60

begin

INSERT INTO [dbo].[DimTime]

([TimeKey]

,[Hour24]

,[Hour24ShortString]

,[Hour24MinString]

,[Hour24FullString]

,[Hour12]

,[Hour12ShortString]

,[Hour12MinString]

,[Hour12FullString]

,[AmPmCode]

,[AmPmString]

,[Minute]

,[MinuteCode]

,[MinuteShortString]

,[MinuteFullString24]

,[MinuteFullString12]

,[HalfHour]

,[HalfHourCode]

,[HalfHourShortString]

,[HalfHourFullString24]

,[HalfHourFullString12]

,[Second]

,[SecondShortString]

,[FullTimeString24]

,[FullTimeString12]

,[FullTime])

select

(@hour*10000) + (@minute*100) + @second as TimeKey,

@hour as [Hour24],

right('0'+convert(varchar(2),@hour),2) [Hour24ShortString],

right('0'+convert(varchar(2),@hour),2)+':00' [Hour24MinString],

right('0'+convert(varchar(2),@hour),2)+':00:00' [Hour24FullString],

@hour%12 as [Hour12],

right('0'+convert(varchar(2),@hour%12),2) [Hour12ShortString],

right('0'+convert(varchar(2),@hour%12),2)+':00' [Hour12MinString],

right('0'+convert(varchar(2),@hour%12),2)+':00:00' [Hour12FullString],

@hour/12 as [AmPmCode],

case when @hour<12 then 'AM' else 'PM' end as [AmPmString],

@minute as [Minute],

(@hour*100) + (@minute) [MinuteCode],

right('0'+convert(varchar(2),@minute),2) [MinuteShortString],

right('0'+convert(varchar(2),@hour),2)+':'+

right('0'+convert(varchar(2),@minute),2)+':00' [MinuteFullString24],

right('0'+convert(varchar(2),@hour%12),2)+':'+

right('0'+convert(varchar(2),@minute),2)+':00' [MinuteFullString12],

@minute/30 as [HalfHour],

(@hour*100) + ((@minute/30)*30) [HalfHourCode],

right('0'+convert(varchar(2),((@minute/30)*30)),2) [HalfHourShortString],

right('0'+convert(varchar(2),@hour),2)+':'+

right('0'+convert(varchar(2),((@minute/30)*30)),2)+':00' [HalfHourFullString24],

right('0'+convert(varchar(2),@hour%12),2)+':'+

right('0'+convert(varchar(2),((@minute/30)*30)),2)+':00' [HalfHourFullString12],

@second as [Second],

right('0'+convert(varchar(2),@second),2) [SecondShortString],

right('0'+convert(varchar(2),@hour),2)+':'+

right('0'+convert(varchar(2),@minute),2)+':'+

right('0'+convert(varchar(2),@second),2) [FullTimeString24],

right('0'+convert(varchar(2),@hour%12),2)+':'+

right('0'+convert(varchar(2),@minute),2)+':'+

right('0'+convert(varchar(2),@second),2) [FullTimeString12],

convert(time,right('0'+convert(varchar(2),@hour),2)+':'+

right('0'+convert(varchar(2),@minute),2)+':'+

right('0'+convert(varchar(2),@second),2)) as [FullTime]

set @second=@second+1

end

set @minute=@minute+1

end

set @hour=@hour+1

end